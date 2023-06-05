import contextlib
import os
import pathlib
import shutil
import tempfile
from unittest.mock import patch
from urllib.parse import urljoin

import requests_mock


def datapath(fname):
    """Return the full path for a testing asset under the tests directory.

    Args:
        fname (str): File name of an asset, relative to the tests directory.
    """
    return pathlib.Path(__file__).parent / fname


@contextlib.contextmanager
def datafile(contents, fname="temp.txt"):
    try:
        d = pathlib.Path(tempfile.mkdtemp())
        path = d / fname
        with open(path, "wt") as fp:
            fp.write(contents)
        yield path
    finally:
        shutil.rmtree(d)


@contextlib.contextmanager
def patch_minio():
    """ Patch Minio client to return canned response.
    """

    patch_env = patch.dict(
        os.environ, {"ACCESS_KEY": "accesskey",
                     "SECRET_KEY": "secretkey"})
    with patch_env, patch("uploader.store.Minio") as cls:
        instance = cls.return_value
        instance.presigned_get_object.return_value = \
            "http://upload-host/bucket/file.txt?ExpiresIn=3600"

        yield instance


@contextlib.contextmanager
def patch_drs_filer(base_url):
    """ Patch REST calls to DRS-filer to return canned response.
    """
    with requests_mock.Mocker() as m:
        m.post(urljoin(base_url, "ga4gh/drs/v1/objects"),
               text="dummy_id")
        yield m
