import logging

from .crypt4gh_wrapper import get_key_from_bytes

logger = logging.getLogger(__name__)


def get_server_pubkeys(client):
    """ Retrieve server public keys, advertised in /service-info.
    """
    crypt4gh_info = client.get_service_info().get("crypt4gh", {})
    pubkeys = [
        get_key_from_bytes(key) for key in crypt4gh_info.get("pubkey", [])
    ]
    logger.info("Loaded %d server public keys", len(pubkeys))
    return pubkeys
