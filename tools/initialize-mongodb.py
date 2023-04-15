import argparse
import pymongo


def _initialize_database(host):
    client = pymongo.MongoClient(f'mongodb://{host}:27017/')
    db = client['drsStore']
    # Create empty collections, as required for DRS-filer to work. At a future
    # stage, we could initialize these collections with dummy data for testing.
    _try_create(db, 'objects')
    _try_create(db, 'service_info')


def _parse_args():
    parser = argparse.ArgumentParser(
        description='Create MongoDB database and collections')
    parser.add_argument('--host', default='localhost', help='MongoDB hostname')
    return parser.parse_args()


def _try_create(db, name):
    try:
        db.create_collection(name)
        print(f"Empty collection {name!r} created.")
    except pymongo.errors.CollectionInvalid:
        print(f"Collection {name!r} already exists, ignoring.")


if __name__ == "__main__":
    args = _parse_args()
    _initialize_database(args.host)
