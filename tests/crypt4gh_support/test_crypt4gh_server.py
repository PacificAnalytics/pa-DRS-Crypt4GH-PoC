from pathlib import Path
from unittest.mock import Mock, ANY

import pytest

from drs_filer.crypt4gh_support import server
from drs_filer.crypt4gh_support.config import Crypt4GHConfig
from drs_filer.crypt4gh_support.server import (
    _parse_object_url, _download_to_file, _reencrypt_file, _upload_file,
    reencrypt_access_url
)


def test_download_to_file():
    temp_d = Path("/a/b/c")
    client = Mock()
    fname = _download_to_file(client, "foo", temp_d)

    assert fname.parent == temp_d
    client.download_file.assert_called_once_with("foo", fname)


def test_parse_object_url():
    url = "https://my-object-store/a/b/c/bucket/object.id"
    assert _parse_object_url(url) == "object.id"


@pytest.fixture
def patch_reencrypt(monkeypatch):
    new = Mock()
    monkeypatch.setattr(server, "reencrypt", new)
    yield new


def test_reencrypt_file(patch_reencrypt, tmp_path):

    # GIVEN
    server_seckey = b"seckey"
    client_pubkey = b"pubkey"

    fname = tmp_path / "file.txt"
    fname.touch()

    # WHEN
    fname_enc = _reencrypt_file(fname, server_seckey, client_pubkey)

    # THEN
    assert fname_enc.parent == fname.parent
    assert fname_enc != fname
    patch_reencrypt.assert_called_once_with(
        server_seckey, client_pubkey, ANY, ANY)


def test_upload_file():
    client = Mock()
    _upload_file(client, "foo.txt")
    client.upload_file.assert_called_once_with("foo.txt")


@pytest.fixture
def patch_upload(monkeypatch):
    yield _patch_helper(
        monkeypatch, "_upload_file",
        retval="http://my-object-store.com/bucket/new.bin")


@pytest.fixture
def patch_download(monkeypatch):
    yield _patch_helper(
        monkeypatch, "_download_to_file", retval="/a/b/c/orig.txt.enc")


@pytest.fixture
def patch_reencrypt_file(monkeypatch):
    yield _patch_helper(
        monkeypatch, "_reencrypt_file", retval="/a/b/c/orig.txt.reenc")


def _patch_helper(monkeypatch, funcname, retval):
    new = Mock(return_value=retval)
    monkeypatch.setattr(server, funcname, new)
    return new


def test_reencrypt_access_url(
        patch_env, patch_upload, patch_download, patch_reencrypt_file):

    # GIVEN
    access_url = {
        "url": "http://my-object-store.com/bucket/orig.txt"
    }
    client_pubkey = b"pubkey"
    crypt4gh_conf = Crypt4GHConfig(
        storage_host="http://my-object-store.com",
        storage_bucket="bucket",
    )

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
    patch_reencrypt_file.assert_called_once_with(
        "/a/b/c/orig.txt.enc", ANY, ANY)
    patch_upload.assert_called_once_with(ANY, "/a/b/c/orig.txt.reenc")
