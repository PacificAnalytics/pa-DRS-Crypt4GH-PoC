__version__ = '0.1.0'

import logging
import os

from flask_pymongo import PyMongo


def _patch_create_mongo_client():
    """Monkey patch _create_mongo_client to allow passing in
    connection details via the `MONGO_URI` environment variable.
    """
    # This is a temporary workaround, to be contributed back to Foca

    import foca.database.register_mongodb
    from foca.database.register_mongodb import _create_mongo_client

    def _patched_create_mongo_client(app, host, port, db):
        logger = logging.getLogger(__name__)
        mongo_uri = os.environ.get("MONGO_URI")
        if mongo_uri:
            # Pass in the connection string
            mongo = PyMongo(app, uri=mongo_uri)
            logger.info("Registered database with connection string %s",
                        mongo_uri)
            return mongo
        else:
            # Dispatch to the generic implementation
            return _create_mongo_client(app, host, port, db)

    # Monkey patch with our new function
    foca.database.register_mongodb._create_mongo_client = \
        _patched_create_mongo_client


_patch_create_mongo_client()
del _patch_create_mongo_client
