import pymongo
import os


def _try_create(db, name):
    try:
        db[name].insert_one({"dummy": "foo"})
        print(f"Empty collection {name!r} created.")
    except pymongo.errors.CollectionInvalid:
        print(f"Collection {name!r} already exists, ignoring.")


if __name__ == "__main__":
    client = pymongo.MongoClient(os.environ["MONGO_URI"])
    # Create empty collections, as required for DRS-filer to work. At a future
    # stage, we could initialize these collections with dummy data for testing.
    _try_create(client.db, 'objects')
    _try_create(client.db, 'service_info')
