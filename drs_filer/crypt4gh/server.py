"""Server code to support Crypt4GH."""

import logging
import os
from urllib.parse import urlparse

from uploader.store import BucketStore
from uploader.crypt4gh_wrapper import get_seckey, reencrypt

from .utils import create_unique_filename, temp_folder

logger = logging.getLogger(__name__)


def _load_store_from_conf(conf):
    # TODO: BucketStore grabs ACCESS_KEY and SECRET_KEY from the
    # environment. This should be changed to pass in these values explicitly.
    client = BucketStore(
        conf["storage_host"], conf["storage_bucket"], secure=False)
    return client


def _download_to_file(client, object_id, temp_d):
    fname = create_unique_filename(temp_d)
    client.download_file(object_id, fname)
    logger.info("Downloaded encrypted resource to %s", fname)
    return fname


def _reencrypt_file(fname, server_seckey, client_pubkey):
    """Reencrypt file with given server seckey/client pubkey.

    Args:
        fname: The encrypted file to be reencrypted.
        server_seckey (bytes): The secret key of the server.
        requester_pubkey (bytes): The public key of the requester.

    Returns:
        fname_enc: The filename of the reencrypted file (created in the same
        directory as the original file).

    """
    fname_enc = create_unique_filename(fname.parent)
    with open(fname, "rb") as original, open(fname_enc, "wb") as enc:
        reencrypt(server_seckey, client_pubkey, original, enc)
    logger.info("Re-encrypted resource to %s", fname_enc)
    return fname_enc


def reencrypt_access_url(access_url, client_pubkey, crypt4gh_conf):
    """Re-encrypt data at given access URL.

    Args:
        access_url: Current access URL data. The "url" key points to the file
        data owned by the server (i.e. encrypted with the public key of the
        server)
        client_pubkey (bytes): Public key of the client.
        crypt4gh_conf: Crypt4gh-specific configuration.

    Returns:
        updated_access_url: Updated access URL data. The "url" key points to
        the file data that was re-encrypted for the client.

    """
    # TODO: Not efficient to load these from disk every time a URL needs to be
    # rewritten, perhaps cache on flask context?
    client = _load_store_from_conf(crypt4gh_conf)
    server_seckey = get_seckey(crypt4gh_conf["seckey_path"])

    bucket_object_id = urlparse(access_url["url"]).path
    object_id = os.path.split(bucket_object_id)[-1]
    logger.info("Re-encrypting object ID %s", object_id)

    with temp_folder() as temp_d:
        # Download
        resource = _download_to_file(client, object_id, temp_d)

        # Reencrypt
        resource_enc = _reencrypt_file(resource, server_seckey, client_pubkey)

        # Upload
        url = client.upload_file(resource_enc)
        logger.info("Uploaded resource to %s", url)

    access_url["url"] = url
    return access_url
