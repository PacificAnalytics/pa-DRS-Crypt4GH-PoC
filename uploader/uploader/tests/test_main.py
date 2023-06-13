import click
import pytest

from ..crypt4gh_wrapper import get_pubkey, get_seckey
from ..drs import DRSClient
from ..main import main, _load_crypt4gh_keys

from .testing_utils import datafile, datapath, patch_drs_filer, patch_minio


def test_main(cli_runner):

    with patch_minio() as minio_client, \
         patch_drs_filer("http://drs.url") as drs_client, \
         datafile("foo") as path:

        # WHEN
        result = cli_runner.invoke(
            main, [
                "--drs-url", "http://drs.url",
                "--storage-url", "http://storage.url",
                "--bucket", "some-bucket",
                "--insecure",
                "--desc", "integration test object",
                str(path)
            ])

        # THEN, (a) check that command exited normally
        assert result.exit_code == 0

        # THEN, (b) check that bytes were uploaded
        minio_client.put_object.assert_called_once()
        call_args = minio_client.put_object.call_args
        assert call_args[0][0] == "some-bucket"
        assert call_args[0][1] == "temp.txt"

        # THEN, (c) check that metadata was registered
        assert drs_client.call_count == 1
        payload = drs_client.request_history[-1].json()
        assert payload["name"] == "temp.txt"
        assert payload["description"] == "integration test object"


def test_main_encrypted(cli_runner):

    with patch_minio() as minio_client, \
         patch_drs_filer("http://drs.url", crypt4gh=True), \
         datafile("foo") as path:

        # WHEN
        result = cli_runner.invoke(
            main, [
                "--drs-url", "http://drs.url",
                "--storage-url", "http://storage.url",
                "--bucket", "some-bucket",
                "--insecure",
                "--desc", "integration test object",
                "--encrypt",
                "--client-sk", datapath("client-sk.key"),
                str(path)
            ])

        # THEN, (a) check that command exited normally
        assert result.exit_code == 0

        # THEN, (b) check that bytes were uploaded
        minio_client.put_object.assert_called_once()
        call_args = minio_client.put_object.call_args
        assert call_args[0][0] == "some-bucket"
        assert call_args[0][1] == "temp.txt.crypt4gh"


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
