"""Crypt4gh-related utilities for the uploader client."""

from base64 import b64decode
import logging

logger = logging.getLogger(__name__)


def get_server_pubkey(client):
    """Retrieve server public key, advertised in /service-info.

    Args:
        client (DRSClient) : DRS server client

    Returns:
        The public key of the server, or None if the server does not
        advertise crypt4gh support.
    """
    crypt4gh_info = client.get_service_info().get("crypt4gh", {})

    pubkey_b64 = crypt4gh_info.get("pubkey", None)
    if not pubkey_b64:
        return None

    pubkey_decoded = b64decode(pubkey_b64)
    logger.info("Loaded server public key: %s", pubkey_b64)
    return pubkey_decoded
