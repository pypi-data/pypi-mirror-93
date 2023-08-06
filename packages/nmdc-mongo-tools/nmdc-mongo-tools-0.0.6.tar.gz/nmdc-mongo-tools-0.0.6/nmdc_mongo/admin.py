"""
Usage:
```
from nmdc_mongo.admin import ensure_users

ensured = ensure_users(<username>@<domain>)
```

If read-only and read-write usernames created, they appear in the ensured dict, along with generated passwords.

SOMEDAY MAYBE add `authenticationRestrictions` of IP address / CIDR range per user.

"""

import itertools
import os
import random

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
admin_client = MongoClient(
    host=os.getenv("NMDC_MONGO_HOST"),
    username="nmdc-admin",
    password=os.getenv("NMDC_MONGO_ADMIN_PWD"),
)
admin_db = admin_client["admin"]


def create_ro_user(username, pwd=""):
    admin_db.command(
        "createUser",
        f"{username}",
        pwd=pwd,
        roles=[
            {"role": "read", "db": f"{username}_scratch"},
            {"role": "read", "db": f"{username}_dev"},
            {"role": "read", "db": f"{username}_share"},
        ],
    )


def create_rw_user(username, pwd=""):
    admin_db.command(
        "createUser",
        f"{username}",
        pwd=pwd,
        roles=[
            {"role": "readWrite", "db": f"{username}_scratch"},
            {"role": "readWrite", "db": f"{username}_dev"},
            {"role": "readWrite", "db": f"{username}_share"},
        ],
    )


def usernames():
    return sorted(doc["user"] for doc in admin_db.command("usersInfo")["users"])


def username_stems():
    return sorted({u[:-3] for u in usernames() if u.endswith("_rw")})


def grant_read_roles_for_share_dbs(username):
    stems = username_stems()
    if not stems:
        return
    admin_db.command(
        "grantRolesToUser",
        username,
        roles=[{"role": "read", "db": f"{stem}_share"} for stem in username_stems()],
    )


def ensure_share_reads():
    for (stem, suffix) in itertools.product(username_stems(), ("_ro", "_rw")):
        username = stem + suffix
        grant_read_roles_for_share_dbs(username)


def nwordspass(n=5, sep="-", words_file="/usr/share/dict/words"):
    with open(words_file) as f:
        lines = f.readlines()
    words = set(line.strip().lower() for line in lines)
    result = sep.join(random.sample(words, n))
    return result


def ensure_users(email):
    username_stem = email.split("@")[0]
    names = set(usernames())
    result = {"email": email}
    user_ro = username_stem + "_ro"
    if user_ro not in names:
        pwd = nwordspass()
        create_ro_user(user_ro, pwd=pwd)
        result[user_ro] = pwd
    user_rw = username_stem + "_rw"
    if user_rw not in names:
        pwd = nwordspass()
        create_rw_user(user_rw, pwd=pwd)
        result[user_rw] = pwd
    ensure_share_reads()
    return result


def reset_database_schema(db, target_collection_names, collschemas):
    for coll_name in target_collection_names:
        if coll_name not in db.list_collection_names():
            print("creating", coll_name)
            db.create_collection(
                coll_name, validator={"$jsonSchema": collschemas[coll_name]}
            )
            db[coll_name].create_index("id", unique=True)
        else:
            print("updating", coll_name)
            db.command(
                "collMod", coll_name, validator={"$jsonSchema": collschemas[coll_name]}
            )
