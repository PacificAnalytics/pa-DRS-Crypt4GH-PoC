import contextlib
from unittest.mock import patch

from ..store import BucketStore
from .testing_utils import datafile


@contextlib.contextmanager
def patch_boto3():
    """Patch Boto3 client to return canned response."""

    with patch("uploader.store._configure_client") as configure_client:
        client = configure_client.return_value
        client.generate_presigned_url.return_value = \
            "http://example.com/myfile.txt?Expiry=3600"
        yield client


def test_upload_file():
    with patch_boto3() as client, datafile("foo") as path:
        store = BucketStore("bucket")

        obj_url = store.upload_file(path, "file.txt")

        assert obj_url == "http://example.com/myfile.txt?Expiry=3600"
        client.upload_file.assert_called_once_with(
            path, "bucket", "file.txt",
        )


def test_download_file():
    with patch_boto3() as client:
        store = BucketStore("bucket")
        store.download_file("fileid", "path/to/save.txt")

    client.download_file.assert_called_once_with(
        "bucket", "fileid", "path/to/save.txt"
    )
