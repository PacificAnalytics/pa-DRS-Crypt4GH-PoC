from base64 import b64encode

from ..crypt4gh_client import get_server_pubkey
from ..drs import DRSClient
from .testing_utils import patch_service_info, SERVICE_INFO_CRYPT4GH


def test_get_server_pubkey():
    client = DRSClient("http://drs.url")
    with patch_service_info("http://drs.url"):
        pubkey = get_server_pubkey(client)
    assert b64encode(pubkey).decode("ascii") == \
        SERVICE_INFO_CRYPT4GH["crypt4gh"]["pubkey"]


def test_get_server_pubkey_not_advertised():
    client = DRSClient("http://drs.url")
    with patch_service_info("http://drs.url", crypt4gh=False):
        pubkey = get_server_pubkey(client)
    assert pubkey is None
