import os
from pathlib import Path
from unittest.mock import Mock, patch, ANY

from drs_filer.crypt4gh_support.config import Crypt4GHConfig
from drs_filer.crypt4gh_support.utils import temp_folder
from drs_filer.crypt4gh_support.server import (
    _parse_object_url, _download_to_file, _reencrypt_file, _upload_file,
    reencrypt_access_url
)

from uploader.tests.testing_utils import datapath


def test_download_to_file():
    temp_d = Path("/a/b/c")
    client = Mock()
    fname = _download_to_file(client, "foo", temp_d)

    assert fname.parent == temp_d
    client.download_file.assert_called_once_with("foo", fname)


def test_parse_object_url():
    url = "https://my-object-store/a/b/c/bucket/object.id"
    assert _parse_object_url(url) == "object.id"


def test_reencrypt_file():
    server_seckey = b"seckey"
    client_pubkey = b"pubkey"

    with temp_folder() as temp_d, \
         patch("drs_filer.crypt4gh_support.server.reencrypt") as patch_reencrypt:  # noqa

        fname = temp_d / "file.txt"
        fname.touch()

        fname_enc = _reencrypt_file(fname, server_seckey, client_pubkey)

    assert fname_enc.parent == fname.parent
    assert fname_enc != fname
    patch_reencrypt.assert_called_once_with(
        server_seckey, client_pubkey, ANY, ANY)


def test_upload_file():
    client = Mock()
    _upload_file(client, "foo.txt")
    client.upload_file.assert_called_once_with("foo.txt")


def _patch_env():
    # Set up environment variables for running with Crypt4GH support.
    with open(datapath("server-sk.key"), "rt", encoding="utf-8") as fp:
        sec_key = fp.read()
    with open(datapath("server-pk.key"), "rt", encoding="utf-8") as fp:
        pub_key = fp.read()
    return patch.dict(
        os.environ, {"ACCESS_KEY": "accesskey",
                     "SECRET_KEY": "secretkey",
                     "SEC_KEY": sec_key,
                     "PUB_KEY": pub_key})


def _patch_helper(funcname):
    return patch(f"drs_filer.crypt4gh_support.server.{funcname}")


@_patch_env()
@_patch_helper("_upload_file")
@_patch_helper("_reencrypt_file")
@_patch_helper("_download_to_file")
def test_reencrypt_access_url(
        patch_download, patch_reencrypt, patch_upload):

    # GIVEN
    access_url = {
        "url": "http://my-object-store.com/bucket/orig.txt"
    }
    client_pubkey = b"pubkey"
    crypt4gh_conf = Crypt4GHConfig(
        storage_host="my-object-store.com",
        storage_bucket="bucket",
    )

    # Configure patchers
    patch_download.return_value = "/a/b/c/orig.txt.enc"
    patch_reencrypt.return_value = "/a/b/c/orig.txt.reenc"
    patch_upload.return_value = "http://my-object-store.com/bucket/new.bin"

    # WHEN
    new_access_url = reencrypt_access_url(
        access_url, client_pubkey, crypt4gh_conf
    )

    # THEN -- assert that acces_url is not changed and new acces_url is
    # properly set
    assert access_url == {
        "url": "http://my-object-store.com/bucket/orig.txt"
    }  # same as before
    assert new_access_url == {
        "url": "http://my-object-store.com/bucket/new.bin"
    }

    # THEN -- assert helpers are properly called
    patch_download.assert_called_once_with(ANY, "orig.txt", ANY)
    patch_reencrypt.assert_called_once_with("/a/b/c/orig.txt.enc", ANY, ANY)
    patch_upload.assert_called_once_with(ANY, "/a/b/c/orig.txt.reenc")
