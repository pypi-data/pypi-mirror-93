Tools for validation and storage of JSON data using the [NMDC Schema](https://github.com/microbiomedata/nmdc-metadata).

# Getting Started

```
pip install nmdc-mongo-tools
# 
```

Create a `.env` file in your working directory and add the following lines to it:
```
NMDC_JSON_SCHEMA_URL=https://raw.githubusercontent.com/microbiomedata/nmdc-metadata/master/schema/nmdc.schema.json
NMDC_MONGO_HOST=<host>
NMDC_MONGO_USERNAME=<username>
NMDC_MONGO_PWD=<password>
NMDC_MONGO_DBNAME=<database-name>
```

, setting appropriate values for connecting to a MongoDB instance. As an alternative to `NMDC_JSON_SCHEMA_URL`, you may
set `NMDC_JSON_SCHEMA_FILE` to be the path to your local copy of the NMDC Schema JSON file. You may also set your
environment variables any other way -- the `.env`-file approach is supported but not required.

Then, import from the `nmdc_mongo` package, e.g.

```python
from nmdc_mongo import get_db

db = get_db()
```