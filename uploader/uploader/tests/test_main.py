from unittest.mock import patch

import click
import pytest

from ..crypt4gh_wrapper import get_pubkey, get_seckey
from ..drs import DRSClient
from ..main import main, _load_crypt4gh_keys
from ..store import BucketStore

from .testing_utils import datafile, datapath, patch_drs_filer


def test_main(cli_runner):

    with patch("uploader.main.BucketStore", spec=BucketStore) as store_cls, \
         patch_drs_filer("http://drs.url") as drs_client, \
         datafile("foo") as path:

        # GIVEN
        store = store_cls.return_value
        store.upload_file.return_value = "http://example.com/myfile"

        # WHEN
        result = cli_runner.invoke(
            main, [
                "--drs-url", "http://drs.url",
                "--storage-url", "http://storage.url",
                "--bucket", "some-bucket",
                "--desc", "integration test object",
                str(path)
            ])

        # THEN, (a) check that command exited normally
        assert result.exit_code == 0

        # THEN, (b) check that bytes were uploaded
        store.upload_file.assert_called_once()
        call_args = store.upload_file.call_args[0]
        assert call_args[0].endswith("temp.txt")

        # THEN, (c) check that metadata was registered
        assert drs_client.call_count == 1
        payload = drs_client.request_history[-1].json()
        assert payload["name"] == "temp.txt"
        assert payload["description"] == "integration test object"


def test_main_encrypted(cli_runner):

    with patch("uploader.main.BucketStore", spec=BucketStore) as store_cls, \
         patch_drs_filer("http://drs.url", crypt4gh=True), \
         datafile("foo") as path:

        # GIVEN
        store = store_cls.return_value
        store.upload_file.return_value = "http://example.com/myfile"

        # WHEN
        result = cli_runner.invoke(
            main, [
                "--drs-url", "http://drs.url",
                "--storage-url", "http://storage.url",
                "--bucket", "some-bucket",
                "--desc", "integration test object",
                "--encrypt",
                "--client-sk", datapath("client-sk.key"),
                str(path)
            ])

        # THEN, (a) check that command exited normally
        assert result.exit_code == 0

        # THEN, (b) check that bytes were uploaded
        store.upload_file.assert_called_once()
        call_args = store.upload_file.call_args[0]
        assert call_args[0].endswith("temp.txt.crypt4gh")


def test_load_crypt4gh_keys_no_server_crypt4gh():
    client = DRSClient("http://drs.url")
    client_sk = datapath("client-sk.key")
    with patch_drs_filer("http://drs.url", crypt4gh=False):
        with pytest.raises(click.ClickException,
                           match="server does not advertise"):
            _load_crypt4gh_keys(client, client_sk)


def test_load_crypt4gh_keys_no_client_sk():
    client = DRSClient("http://drs.url")
    client_sk = datapath("does-not-exist.key")
    with patch_drs_filer("http://drs.url", crypt4gh=True):
        with pytest.raises(click.ClickException,
                           match="Could not load client secret key"):
            _load_crypt4gh_keys(client, client_sk)


def test_load_crypt4gh():
    client = DRSClient("http://drs.url")
    client_sk = datapath("client-sk.key")
    with patch_drs_filer("http://drs.url", crypt4gh=True):
        server_pubkey, client_seckey = \
            _load_crypt4gh_keys(client, client_sk)

    expected_server_pubkey = get_pubkey(datapath("server-pk.key"))
    expected_client_seckey = get_seckey(datapath("client-sk.key"))
    assert server_pubkey == expected_server_pubkey
    assert client_seckey == expected_client_seckey
