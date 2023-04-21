import os
from urllib.parse import urlparse, urlunparse

from minio import Minio


def configure_client(endpoint, secure=True):
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


def upload_file(endpoint, bucket, file_path, name, secure=True):
    client = configure_client(endpoint, secure)
    with open(file_path, 'rb') as fp:
        client.put_object(
            bucket, name, fp, os.stat(file_path).st_size)
    return _url_for_object(client, bucket, name)
