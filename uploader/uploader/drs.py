""" DRS metadata request handling.
"""
from dataclasses import dataclass
import datetime
import json
import os
from urllib.parse import urljoin

import requests

from .files import compute_sha256, compute_size


@dataclass
class DRSMetadata:
    name: str  # The name of the object, used to identify it
    checksum: str  # SHA-256 checksum
    size: int  # Size, in bytes
    url: str = ""  # URL to retrieve bytes
    description: str = ""  # Optional description

    @classmethod
    def from_file(cls, fpath, url="", description=""):
        return cls(
            name=os.path.basename(fpath),
            checksum=compute_sha256(fpath),
            size=compute_size(fpath),
            url=url,
            description=description,
        )


class DRSClient:

    def __init__(self, drs_url):
        self._drs_url = drs_url

    def post_metadata(self, metadata):
        request_data = _create_request_data(metadata)
        objects_endpoint = urljoin(self._drs_url, "ga4gh/drs/v1/objects")
        response = requests.post(
            objects_endpoint,
            headers={"Content-Type": "application/json"},
            data=json.dumps(request_data))

        response.raise_for_status()
        return response.content.decode("ascii").strip()


def _create_request_data(drs_metadata):
    now_datetime = datetime.datetime.now().isoformat()
    request_data = {
        "access_methods": [
            {
                "access_url": {
                    "headers": [],
                    "url": drs_metadata.url,
                },
                "type": "s3",
            }
        ],
        "aliases": [],
        "checksums": [{
            "checksum": drs_metadata.checksum,
            "type": "sha-256"
        }],
        "description": drs_metadata.description,
        "mime_type": "application/json",
        "name": drs_metadata.name,
        "size": drs_metadata.size,
        "created_time": now_datetime,
        "updated_time": now_datetime,
        "version": "1",
    }
    return request_data


def post_metadata(drs_metadata, base_url):
    return DRSClient(base_url).post_metadata(drs_metadata)
    request_data = _create_request_data(drs_metadata)
    objects_endpoint = urljoin(base_url, "ga4gh/drs/v1/objects")
    response = requests.post(
        objects_endpoint,
        headers={"Content-Type": "application/json"},
        data=json.dumps(request_data))

    response.raise_for_status()
    return response.content.decode("ascii").strip()
