import logging
import os
from urllib.parse import urlparse, urlunparse

from minio import Minio

logger = logging.getLogger(__name__)


class BucketStore:
    """ File store using an S3 or Minio bucket.
    """

    def __init__(self, endpoint, bucket, secure=True):
        self._client = _configure_client(endpoint, secure)
        self._bucket = bucket

    def upload_file(self, file_path, name=None):
        """ Upload a file to the store.

        Parameters
        ----------
        file_path : str
            File path to upload.
        name : str, optional
            Optionally, a name under which to register the file. If not set,
            defaults to the file name.

        Returns
        -------
        url : str
            A URL that can be used to retrieve the file from the storage.

        """
        name = name or os.path.basename(file_path)
        with open(file_path, 'rb') as fp:
            logger.debug("Uploading file %s", file_path)
            self._client.put_object(
                self._bucket, name, fp, os.stat(file_path).st_size)

        url = _url_for_object(self._client, self._bucket, name)
        logger.debug("Finished file upload. URL: %s", url)
        return url

    def download_file(self, file_id, file_path):
        """Download file from the store.

        Args:
            file_id (str) : Object ID (in the store) of the file to download.
            file_path (str) : Where to store the downloaded file.

        """
        self._client.fget_object(self._bucket, file_id, file_path)


def _configure_client(endpoint, secure=True):
    client = Minio(endpoint,
                   access_key=os.environ["ACCESS_KEY"],
                   secret_key=os.environ["SECRET_KEY"],
                   secure=secure)
    return client


def _url_for_object(client, bucket, name):
    url = client.presigned_get_object(bucket, name)
    return _remove_query_string(url)


def _remove_query_string(url):
    parsed_url = urlparse(url)
    return urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        '',  # remove the query string
        parsed_url.fragment
    ))
