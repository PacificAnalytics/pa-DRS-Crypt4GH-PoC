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
        conf.storage_bucket,
        endpoint=conf.storage_host
    )
    return client


def _parse_object_url(url):
    """Return object ID from object URL."""
    bucket_object_id = urlparse(url).path
    object_id = os.path.split(bucket_object_id)[-1]
    return object_id


def _download_to_file(client, object_id, temp_d):
    fname = create_unique_filename(temp_d)
    client.download_file(object_id, fname)
    logger.info("Downloaded encrypted resource to %s", fname)
    return fname


def _reencrypt_file(fname, server_seckey, client_pubkey):
    """Reencrypt file with given server seckey/client pubkey."""
    fname_enc = create_unique_filename(fname.parent)
    with open(fname, "rb") as original, open(fname_enc, "wb") as enc:
        reencrypt(server_seckey, client_pubkey, original, enc)
    logger.info("Re-encrypted resource to %s", fname_enc)
    return fname_enc


def _upload_file(client, fname):
    url = client.upload_file(fname)
    logger.info("Uploaded resource to %s", url)
    return url


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
    server_seckey = get_seckey(crypt4gh_conf.seckey_path)

    object_id = _parse_object_url(access_url["url"])
    logger.info("Re-encrypting object ID %s", object_id)

    with temp_folder() as temp_d:
        # Download original file data, reencrypt, and upload again
        resource = _download_to_file(client, object_id, temp_d)
        resource_enc = _reencrypt_file(resource, server_seckey, client_pubkey)
        url = _upload_file(client, resource_enc)

    return {  # copy of access_url with modified url entry
        **access_url,
        "url": url
    }


def presign_access_url(access_url, crypt4gh_conf):
    """Generate presigned URL for given access URL data.

    Args:
        access_url: Current access URL data. The "url" key points to the file.
        crypt4gh_conf: Crypt4gh-specific configuration.

    Returns:
        updated_access_url: Updated access URL data. The "url" key is a signed
        URL providing access to the data.

    """
    client = _load_store_from_conf(crypt4gh_conf)

    object_id = _parse_object_url(access_url["url"])
    logger.info("Generating presigned URL for object ID %s", object_id)
    url = client.generate_presigned_url(object_id)

    return {  # copy of access_url with modified url entry
        **access_url,
        "url": url
    }
