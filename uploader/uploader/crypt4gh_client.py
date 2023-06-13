"""Crypt4gh-related utilities for the uploader client."""

from base64 import b64decode
import logging

logger = logging.getLogger(__name__)


class KeyError(Exception):
    """Generic error if server pubkey could not be loaded."""


def get_server_pubkey(client):
    """Retrieve server public key, advertised in /service-info.

    Args:
        client (DRSClient) : DRS server client

    Returns:
        The public key of the server.
    """
    try:
        crypt4gh_info = client.get_service_info()["crypt4gh"]
        pubkey_b64 = crypt4gh_info["pubkey"]
        pubkey_decoded = b64decode(pubkey_b64)
        logger.info("Loaded server public key: %s", pubkey_b64)
    except Exception as e:
        raise KeyError() from e
    return pubkey_decoded
