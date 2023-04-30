import logging

from .crypt4gh_wrapper import get_key_from_bytes

logger = logging.getLogger(__name__)


def get_server_pubkey(client):
    """ Retrieve server public key, advertised in /service-info.
    """
    crypt4gh_info = client.get_service_info().get("crypt4gh", {})
    pubkey_b64 = crypt4gh_info.get("pubkey")
    pubkey_decoded = get_key_from_bytes(pubkey_b64)
    logger.info("Loaded server public key: %s", pubkey_b64)
    return pubkey_decoded
