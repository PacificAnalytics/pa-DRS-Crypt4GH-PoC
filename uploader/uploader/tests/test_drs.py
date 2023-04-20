import datetime

from ..drs import _create_request_data, post_metadata
from .testing_utils import datafile


def _is_iso8601(s):
    try:
        datetime.datetime.fromisoformat(s)
        return True
    except ValueError:
        return False


def test_create_request_data():
    name = "obj"
    description = "an object"
    checksum = "1be7aaf1938cc19af7d2fdeb48a11c381dff8a98d4c4b47b3b0a5044a5255c04"  # noqa

    with datafile("test file data") as fname:
        rdata = _create_request_data(fname, name, description)
        assert rdata["name"] == name
        assert rdata["description"] == description
        assert rdata["checksums"][0]["checksum"] == checksum
        assert rdata["size"] == 14
        assert _is_iso8601(rdata["created_time"])
        assert _is_iso8601(rdata["updated_time"])


def test_post_metadata(requests_mock):
    requests_mock.post("http://localhost:8080/ga4gh/drs/v1/objects",
                       text="dummy_id")
    with datafile("test file data") as fname:
        response = post_metadata(fname, "foo", "http://localhost:8080")
    assert response == "dummy_id"
