import pymongo
import os
from urllib.parse import quote_plus

def _try_create(db, name):
    try:
        collection = db[name]
        print(f"Empty collection {name!r} created.")
    except pymongo.errors.CollectionInvalid:
        print(f"Collection {name!r} already exists, ignoring.")

if __name__ == "__main__":
    user = quote_plus(os.environ["MONGO_USERNAME"])
    passwd = quote_plus(os.environ["MONGO_PASSWORD"])
    host = quote_plus(os.environ["MONGO_HOST"])
    db = quote_plus(os.environ["MONGO_DBNAME"])
    client = pymongo.MongoClient(
        f'mongodb://{user}:{passwd}@{host}:27017/{db}?replicaSet=pa-drs-crypt4gh-poc-mongodb&ssl=false'
    )
    db = client[os.environ["MONGO_DBNAME"]]
    # Create empty collections, as required for DRS-filer to work. At a future
    # stage, we could initialize these collections with dummy data for testing.
    _try_create(db, 'objects')
    _try_create(db, 'service_info')
