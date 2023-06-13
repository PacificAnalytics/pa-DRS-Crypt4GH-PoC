from pathlib import Path
from unittest.mock import Mock, patch, ANY

from drs_filer.crypt4gh.utils import temp_folder
from drs_filer.crypt4gh.server import (
    _download_to_file, _reencrypt_file, reencrypt_access_url
)


def test_download_to_file():
    temp_d = Path("/a/b/c")
    client = Mock()
    fname = _download_to_file(client, "foo", temp_d)

    assert fname.parent == temp_d
    client.download_file.assert_called_once_with("foo", fname)


def test_reencrypt_file():
    server_seckey = b"seckey"
    client_pubkey = b"pubkey"

    with patch("drs_filer.crypt4gh.server.reencrypt") as patch_reencrypt, \
         temp_folder() as temp_d:

        fname = temp_d / "file.txt"
        fname.touch()

        fname_enc = _reencrypt_file(fname, server_seckey, client_pubkey)

    assert fname_enc.parent == fname.parent
    assert fname_enc != fname
    patch_reencrypt.assert_called_once_with(
        server_seckey, client_pubkey, ANY, ANY)
