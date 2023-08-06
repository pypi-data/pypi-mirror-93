import concurrent
import json
import os
import re
from datetime import datetime
from itertools import tee

from dotenv import load_dotenv
import jsonschema
import requests
from mongospawn.schema import dbschema_from_file, collschemas_for, dbschema_from_str
from pymongo import ReplaceOne, MongoClient
from toolz import (
    assoc_in,
    compose,
    dissoc,
    keyfilter,
    get_in,
    identity,
)
from tqdm.notebook import tqdm


load_dotenv()
nmdc_json_schema_filepath = os.getenv("NMDC_JSON_SCHEMA_FILE")
if nmdc_json_schema_filepath is None:
    d = requests.get(os.getenv("NMDC_JSON_SCHEMA_URL")).json()
    dbschema = dbschema_from_str(json.dumps(d))
else:
    dbschema = dbschema_from_file(nmdc_json_schema_filepath)
collschemas = collschemas_for(dbschema)


def get_db(dbname):
    client = MongoClient(
        host=os.getenv("NMDC_MONGO_HOST"),
        username=os.getenv("NMDC_MONGO_USERNAME"),
        password=os.getenv("NMDC_MONGO_PWD"),
    )
    return client[dbname]


def reset_database(db):
    for coll_name in collschemas:
        db.drop_collection(coll_name)
        db.create_collection(
            coll_name, validator={"$jsonSchema": collschemas[coll_name]}
        )
        db[coll_name].create_index("id", unique=True)


def jsonschema_for(collection_name=None):
    if collection_name not in set(dbschema["properties"]):
        raise ValueError(
            f'collection_name must be one of {set(dbschema["properties"])}'
        )
    defn = dbschema["properties"][collection_name]["items"]["$ref"].split("/")[-1]
    return dbschema["definitions"][defn]


def conform(doc, collection_name=None):
    """Provides limited, conservative conformance on a docments.

    - If additionalProperties is False, omit any supplied.
    - If a field must be a list of strings, and a lone string is supplied, wrap it in a list.

    """
    if collection_name not in set(dbschema["properties"]):
        raise ValueError(
            f'collection_name must be one of {set(dbschema["properties"])}'
        )
    defn = dbschema["properties"][collection_name]["items"]["$ref"].split("/")[-1]
    schema = dbschema["definitions"][defn]
    if schema.get("additionalProperties") is False:
        doc = pick(list(schema["properties"]), doc)
    for k in list(doc.keys()):
        if (
            isinstance(doc[k], str)
            and schema["properties"].get(k, {}).get("type") == "array"
            and schema["properties"][k]["items"]["type"] == "string"
            and not isinstance(doc[k], list)
        ):
            doc[k] = [doc[k]]
    return doc


def validate(doc, collection_name=None, conform_doc=False):
    if collection_name not in set(dbschema["properties"]):
        raise ValueError(
            f'collection_name must be one of {set(dbschema["properties"])}'
        )
    if conform_doc:
        doc = conform(doc, collection_name=collection_name)
    jsonschema.validate({collection_name: [doc]}, schema=dbschema)
    return doc


def fetch_and_validate_json(resource, collection_name=None, conform_doc=False):
    """Takes a URL or the pre-fetched resource (list or dict)"""
    payload = fetch_json(resource) if isinstance(resource, str) else resource
    validated = []
    if isinstance(payload, list):
        for doc in tqdm(payload):
            validated.append(
                validate(doc, collection_name=collection_name, conform_doc=conform_doc)
            )
    elif isinstance(payload, dict):
        if set(payload) & set(dbschema["properties"]):
            for collection_name, docs in payload.items():
                for doc in tqdm(docs, desc=collection_name):
                    validated.append(
                        validate(
                            doc,
                            collection_name=collection_name,
                            conform_doc=conform_doc,
                        )
                    )
        else:
            validated.append(
                validate(
                    payload, collection_name=collection_name, conform_doc=conform_doc
                )
            )
    else:
        raise ValueError(f"Fetched JSON must be a JSON array or object")
    return validated


def add_to_db(validated, db, collection_name=None):
    if collection_name not in set(dbschema["properties"]):
        raise ValueError(
            f'collection_name must be one of {set(dbschema["properties"])}'
        )
    if isinstance(validated, list):
        db[collection_name].bulk_write(
            [ReplaceOne({"id": v["id"]}, v, upsert=True) for v in validated]
        )
    elif isinstance(validated, dict):
        if set(validated) & set(dbschema["properties"]):
            for collection_name, docs in validated.items():
                db[collection_name].bulk_write(
                    [ReplaceOne({"id": v["id"]}, v, upsert=True) for v in docs]
                )
        else:
            db[collection_name].bulk_write(
                [ReplaceOne({"id": validated["id"]}, validated, upsert=True)]
            )
    else:
        raise ValueError(f"payload must be a list or dict")


def fetch_conform_and_persist(spec, db):
    url = spec["url"]
    collection_name = spec["type"]
    print(f"fetching {url} ({collection_name})")
    payload = fetch_and_validate_json(url, collection_name, conform_doc=True)
    add_to_db(payload, db, collection_name)


def fetch_conform_and_persist_from_manifest(spec, db):
    error_urls = []
    url_manifest = spec["url_manifest"]
    collection_name = spec["type"]
    urls = fetch_json(url_manifest)

    pbar = tqdm(total=len(urls))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {
            executor.submit(
                fetch_and_validate_json, url, collection_name, conform_doc=True
            ): url
            for url in urls
        }
        for future in concurrent.futures.as_completed(future_to_url):
            pbar.update(1)
            url = future_to_url[future]
            try:
                payload = future.result()
            except Exception as e:
                error_urls.append((url, str(e)))
            else:
                add_to_db(payload, db, collection_name)

    pbar.close()
    return error_urls


def fetch_json(url):
    return requests.get(url).json()


def validator_for(collection):
    return collection.options()["validator"]["$jsonSchema"]


def pick(whitelist, d):
    return keyfilter(lambda k: k in whitelist, d)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def coalesce_acronyms(set_name):
    out = ""
    for this_part, next_part in pairwise(set_name.split("_")):
        if len(this_part) == 1 and len(next_part) == 1:
            out += this_part
        elif next_part == "set":
            out += this_part + "_set"
        else:
            out += this_part + "_"
    return out


def snake_case_set_name(object_name):
    first_pass = re.sub(r"(?<!^)(?=[A-Z])", "_", object_name).lower() + "_set"
    return coalesce_acronyms(first_pass)


metaP_field_map = {
    "PeptideSequence": ("peptide_sequence", identity),
    "sum(MASICAbundance)": ("peptide_sum_masic_abundance", int),
    "SpectralCount": ("peptide_spectral_count", int),
    "BestProtein": ("best_protein", identity),
    "min(QValue)": ("min_q_value", float),
}


def map_fields(doc, field_map=None):
    for k_old, todo in field_map.items():
        if k_old in doc:
            k_new, fn = todo
            doc = assoc_in(doc, [k_new], fn(doc[k_old]))
            doc = dissoc(doc, k_old)
    return doc


def correct_metaP_doc(doc):
    if not "has_peptide_quantifications" in doc:
        return doc
    new_items = [
        map_fields(item, metaP_field_map) for item in doc["has_peptide_quantifications"]
    ]
    doc = assoc_in(
        doc,
        ["has_peptide_quantifications"],
        new_items,
    )
    return doc


biosample_dt_pattern = re.compile(
    r"\d{2}-(?P<month>\w+)-\d{2} \d{2}\.\d{2}\.\d{2}\.(?P<ns>\d+) [A|P]M"
)
biosample_dt_format = "%d-%b-%y %I.%M.%S.%f %p"


def order_timestamps(timestamps):
    if not all(isinstance(ts, str) for ts in timestamps):
        raise Exception(f"{timestamps} not strings")
    as_datetimes = []
    for ts in timestamps:
        match = biosample_dt_pattern.search(ts)
        first, month, rest = ts.partition(match.group("month"))
        ts_new = first + month[0] + month[1:].lower() + rest
        ts_new = ts_new.replace(
            match.group("ns"), match.group("ns")[:-3]
        )  # truncate to microseconds
        as_datetimes.append(datetime.strptime(ts_new, biosample_dt_format))
    sorted_dts = sorted(as_datetimes)
    return [dt.strftime(biosample_dt_format) for dt in sorted_dts]


er_xna_pattern = re.compile(r"ER_[D|R]NA_\d+$")


def rstrip_name_ER_ID(d):
    s = get_in(["name"], d)
    s_new = er_xna_pattern.split(s)[0] if er_xna_pattern.search(s) else s
    return assoc_in(d, ["name"], s_new)


def capitalize_location_raw_value(d):
    s = get_in(["location", "has_raw_value"], d)
    s_new = s[0].upper() + s[1:]
    return assoc_in(d, ["location", "has_raw_value"], s_new)


def gold_to_igsn_pipeline():
    return compose(
        capitalize_location_raw_value,
        rstrip_name_ER_ID,
        lambda d: dissoc(d, "_id", "id", "add_date", "mod_date", "identifier"),
    )


def omit(blacklist, d):
    return keyfilter(lambda k: k not in blacklist, d)


def sans_mongo_id(d):
    return omit(["_id"], d)
