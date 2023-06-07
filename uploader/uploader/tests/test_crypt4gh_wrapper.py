from io import BytesIO

import crypt4gh
import pytest

from ..crypt4gh_wrapper import (
    encrypt, get_pubkey, get_pubkey_b64, get_seckey, reencrypt,
    EncryptionError,
)
from .testing_utils import datapath


CLIENT_PUBKEY = get_pubkey(datapath("client-pk.key"))
CLIENT_SECKEY = get_seckey(datapath("client-sk.key"))
RECIPIENT_PUBKEY = get_pubkey(datapath("third-party-pk.key"))
RECIPIENT_SECKEY = get_seckey(datapath("third-party-sk.key"))
SERVER_PUBKEY = get_pubkey(datapath("server-pk.key"))
SERVER_SECKEY = get_seckey(datapath("server-sk.key"))


def test_encrypt():
    # Given (unencrypted data)
    file_data = BytesIO(b"test data")

    # When (encrypt data for recipient)
    encrypted_data = BytesIO()
    encrypt(CLIENT_SECKEY, RECIPIENT_PUBKEY, file_data, encrypted_data)

    # Then (assert recipient can decrypt)
    encrypted_data.seek(0)
    assert _decrypt(encrypted_data, RECIPIENT_SECKEY) == b"test data"


def test_encrypt_fails_gracefully():
    # Given (unencrypted data)
    file_data = BytesIO(b"test data")

    # When (attempting to encrypt with faulty key)
    with pytest.raises(EncryptionError):
        encrypt(b"xyz", RECIPIENT_PUBKEY, file_data, BytesIO())


def test_reencrypt():
    # Given (encrypted data by client for server)
    file_data = BytesIO(b"test data")
    encrypted_data = BytesIO()
    encrypt(CLIENT_SECKEY, SERVER_PUBKEY, file_data, encrypted_data)
    encrypted_data.seek(0)

    # When (reencrypt on server for third-party)
    reencrypted_data = BytesIO()
    reencrypt(
        SERVER_SECKEY, RECIPIENT_PUBKEY, encrypted_data, reencrypted_data)

    # Then (third party can decrypt)
    reencrypted_data.seek(0)
    assert _decrypt(reencrypted_data, RECIPIENT_SECKEY) == b"test data"


def test_reencrypt_fails_gracefully():
    # Given (unencrypted data)
    file_data = BytesIO(b"test data")

    # When (attempting to reencrypt unencrypted data)
    with pytest.raises(EncryptionError):
        reencrypt(SERVER_SECKEY, RECIPIENT_PUBKEY, file_data, BytesIO())


def test_get_pubkey_b64():
    expected_pubkey = "SpqyCbB0/+jZpIhoEADSCg4NJ8b/my3xh9TTNr5zpXs="
    fname = datapath("client-pk.key")
    assert get_pubkey_b64(fname) == expected_pubkey


def _decrypt(buf, seckey):
    buf_out = BytesIO()
    crypt4gh.lib.decrypt([(0, seckey, None)], buf, buf_out)
    return buf_out.getvalue()
