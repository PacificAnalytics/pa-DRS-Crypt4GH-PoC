"""S3-backed file storage."""

import logging
import os
from urllib.parse import urlparse, urlunparse

import botocore
import boto3


logger = logging.getLogger(__name__)


class BucketStore:
    """File store using an S3 or Minio bucket."""

    def __init__(self, bucket, endpoint=None):
        """Create new BucketStore instance.

        Args:
            bucket: The name of the bucket to use.
            endpoint (optional): The hostname and port of the storage server.

        """
        self._client = _configure_client(endpoint)
        self._bucket = bucket

    def upload_file(self, file_path, name=None):
        """Upload a file to the store.

        Args:
            file_path (str): File path to upload.
            name (str, optional): Optionally, a name under which to register
                the file. If not set, defaults to the file name.

        Returns:
            url (str): A URL that can be used to retrieve the file from storage

        """
        name = name or os.path.basename(file_path)

        logger.debug("Uploading file %s", file_path)
        self._client.upload_file(file_path, self._bucket, name)
        logger.debug("Upload finished for file %s", file_path)

        url = self.generate_presigned_url(name)
        logger.debug("Finished file upload. URL: %s", url)
        return url

    def download_file(self, file_id, file_path):
        """Download file from the store.

        Args:
            file_id (str): Object ID (in the store) of the file to download.
            file_path (str): Where to store the downloaded file.

        """
        self._client.download_file(self._bucket, file_id, file_path)

    def generate_presigned_url(self, name):
        """Generate presigned URL for bucket object.
        """
        url = self._client.generate_presigned_url(
            "get_object",
            ExpiresIn=3600,
            Params={'Bucket': self._bucket, 'Key': name},
        )
        return url


def _configure_client(endpoint):
    session = boto3.Session(
        aws_access_key_id=os.environ["ACCESS_KEY"],
        aws_secret_access_key=os.environ["SECRET_KEY"],
    )

    client = session.client(
        "s3",
        endpoint_url=endpoint,
    )

    # Allow for easy creation of URLs to bucket objects.
    config = client._client_config
    config.signature_version = botocore.UNSIGNED

    return client


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
