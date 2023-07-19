import pymongo
import os


def _try_create(db, name):
    try:
        db[name].insert_one({"dummy": "foo"})
        print(f"Empty collection {name!r} created.")
    except Exception:
        print(f"Collection {name!r} already exists, ignoring.")


if __name__ == "__main__":
    client = pymongo.MongoClient(os.environ["MONGO_URI"])
    # Create empty collections, as required for DRS-filer to work. At a future
    # stage, we could initialize these collections with dummy data for testing.
    db = client["drsStore"]
    _try_create(db, 'objects')
    _try_create(db, 'service_info')
