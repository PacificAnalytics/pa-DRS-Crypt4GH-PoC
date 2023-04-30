import logging
import os
from pathlib import Path
import shutil
import tempfile
from urllib.parse import urlparse

from uploader.store import BucketStore
from uploader.crypt4gh_wrapper import get_seckey, reencrypt

logger = logging.getLogger(__name__)


def _load_store_from_conf(conf):
    # TODO: BucketStore grabs ACCESS_KEY and SECRET_KEY from the
    # environment. This should be changed to pass in these values explicitly.
    client = BucketStore(
        conf["storage_host"], conf["storage_bucket"], secure=False)
    return client


def reencrypt_access_url(access_url, client_pubkey, crypt4gh_conf):
    """ Re-encrypt data at given access URL.

    Parameters
    ----------
    access_url : dict
        Current access URL data. The "url" key points to the file data
        owned by the server (i.e. encrypted with the public key of the
        server)
    client_pubkey : dict
        Public key of the client.
    crypt4gh_conf : dict
        Crypt4gh-specific configuration.

    Returns
    -------
    access_url : dict
        Updated access URL data. The "url" key points to the file
        data that was re-encrypted for the client.

    """
    # TODO: Not efficient to load these from disk every time a URL needs to be
    # rewritten, perhaps cache on flask context?
    client = _load_store_from_conf(crypt4gh_conf)
    server_seckey = get_seckey(crypt4gh_conf["seckey_path"])

    bucket_object_id = urlparse(access_url["url"]).path
    object_id = os.path.split(bucket_object_id)[-1]
    logger.info("Re-encrypting object ID %s", object_id)

    temp_folder = Path(tempfile.mkdtemp())
    try:
        # Download
        resource = os.path.join(temp_folder, "filedata.bin")
        client.download_file(object_id, resource)
        logger.info("Downloaded encrypted resource to %s", resource)

        # Reencrypt
        resource_reenc = reencrypt(server_seckey, client_pubkey, resource)
        logger.info("Re-encrypted resource to %s", resource_reenc)

        # Upload
        url = client.upload_file(resource_reenc)
        logger.info("Uploaded resource to %s", url)
    finally:
        shutil.rmtree(temp_folder)
        logger.info("Unlinked temporary folder %s", temp_folder)

    access_url["url"] = url
    return access_url
