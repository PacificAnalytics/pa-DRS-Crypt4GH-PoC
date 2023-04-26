import datetime

from ..drs import DRSClient, DRSMetadata, _create_request_data
from .testing_utils import datafile, patch_drs_filer


def _is_iso8601(s):
    try:
        datetime.datetime.fromisoformat(s)
        return True
    except ValueError:
        return False


def test_drs_metadata():
    checksum = "1be7aaf1938cc19af7d2fdeb48a11c381dff8a98d4c4b47b3b0a5044a5255c04"  # noqa

    with datafile("test file data") as fname:
        drs_metadata = DRSMetadata.from_file(fname)

    assert drs_metadata.checksum == checksum
    assert drs_metadata.size == 14


def test_create_request_data():
    drs_metadata = DRSMetadata(
        name="obj",
        description="an object",
        checksum="xyz",
        url="http://url.to",
        size=25)

    rdata = _create_request_data(drs_metadata)

    assert rdata["name"] == "obj"
    assert rdata["description"] == "an object"
    assert rdata["access_methods"][0]["access_url"]["url"] == "http://url.to"
    assert rdata["checksums"][0]["checksum"] == "xyz"
    assert rdata["size"] == 25
    assert _is_iso8601(rdata["created_time"])
    assert _is_iso8601(rdata["updated_time"])


def test_post_metadata():
    drs_client = DRSClient("http://localhost:8080")
    with patch_drs_filer("http://localhost:8080"), \
         datafile("test file data") as fname:
        drs_meta = DRSMetadata.from_file(fname)
        response = drs_client.post_metadata(drs_meta)
    assert response == "dummy_id"
