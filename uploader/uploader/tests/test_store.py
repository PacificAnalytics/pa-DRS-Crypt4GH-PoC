import os
from unittest.mock import patch

from ..store import BucketStore
from .testing_utils import datafile


@patch.dict(os.environ, {"ACCESS_KEY": "accesskey",
                         "SECRET_KEY": "secretkey"})
def test_upload_file():
    with patch("uploader.store.Minio") as cls, datafile("foo") as path:
        instance = cls.return_value
        instance.presigned_get_object.return_value = \
            "http://upload-host/bucket/file.txt?ExpiresIn=3600"
        store = BucketStore("localhost:9000", "bucket")

        obj_url = store.upload_file(path, "file.txt")

        assert obj_url == "http://upload-host/bucket/file.txt"
        instance.put_object.assert_called_once()
        call_args = instance.put_object.call_args
        assert call_args[0][0] == "bucket"
        assert call_args[0][1] == "file.txt"
        assert call_args[0][3] == 3  # size
