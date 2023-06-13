from base64 import b64encode

import pytest

from ..crypt4gh_client import get_server_pubkey, KeyError
from ..drs import DRSClient
from .testing_utils import patch_drs_filer, SERVICE_INFO_CRYPT4GH


def test_get_server_pubkey():
    client = DRSClient("http://drs.url")
    with patch_drs_filer("http://drs.url"):
        pubkey = get_server_pubkey(client)
    assert b64encode(pubkey).decode("ascii") == \
        SERVICE_INFO_CRYPT4GH["crypt4gh"]["pubkey"]


def test_get_server_pubkey_not_advertised():
    client = DRSClient("http://drs.url")
    with patch_drs_filer("http://drs.url", crypt4gh=False):
        with pytest.raises(KeyError):
            get_server_pubkey(client)
