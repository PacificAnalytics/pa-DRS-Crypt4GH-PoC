import contextlib
import os
from unittest.mock import patch

from ..store import BucketStore
from .testing_utils import datafile


@contextlib.contextmanager
def patch_minio():
    """Patch Minio client to return canned response."""

    patch_env = patch.dict(
        os.environ, {"ACCESS_KEY": "accesskey",
                     "SECRET_KEY": "secretkey"})
    with patch_env, patch("uploader.store.Minio") as cls:
        instance = cls.return_value
        instance.presigned_get_object.return_value = \
            "http://upload-host/bucket/file.txt?ExpiresIn=3600"

        yield instance


def test_upload_file():
    with patch_minio() as client, datafile("foo") as path:
        store = BucketStore("localhost:9000", "bucket")

        obj_url = store.upload_file(path, "file.txt")

        assert obj_url == "http://upload-host/bucket/file.txt"
        client.put_object.assert_called_once()
        call_args = client.put_object.call_args
        assert call_args[0][0] == "bucket"
        assert call_args[0][1] == "file.txt"
        assert call_args[0][3] == 3  # size


def test_download_file():
    with patch_minio() as client:
        store = BucketStore("localhost:9000", "bucket")
        store.download_file("fileid", "path/to/save.txt")
    client.fget_object.assert_called_once()
    call_args = client.fget_object.call_args
    assert call_args[0][0] == "bucket"
    assert call_args[0][1] == "fileid"
    assert call_args[0][2] == "path/to/save.txt"
