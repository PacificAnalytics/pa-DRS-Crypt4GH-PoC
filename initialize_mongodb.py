import pymongo
import os

def _try_create(db, name):
    try:
        db.create_collection(name)
        print(f"Empty collection {name!r} created.")
    except pymongo.errors.CollectionInvalid:
        print(f"Collection {name!r} already exists, ignoring.")

if __name__ == "__main__":
    client = pymongo.MongoClient(f'mongodb://{os.environ["MONGO_HOST"]}:27017/', os.environ["MONGO_USERNAME"], os.environ["MONGO_PASSWORD"])
    db = client[os.environ["MONGO_DBNAME"]]
    # Create empty collections, as required for DRS-filer to work. At a future
    # stage, we could initialize these collections with dummy data for testing.
    _try_create(db, 'objects')
    _try_create(db, 'service_info')
