""" DRS metadata request handling.
"""

import datetime
import json
import requests
from urllib.parse import urljoin

from .files import compute_sha256, compute_size


def _create_request_data(fname, name, description):
    now_datetime = datetime.datetime.now().isoformat()
    request_data = {
        "access_methods": [
            {
                "access_url": {
                    "headers": [],
                    "url": "http://localhost:9000/mybucket/ex.pdf",
                },
                "type": "s3",
            }
        ],
        "aliases": [],
        "checksums": [{
            "checksum": compute_sha256(fname),
            "type": "sha-256"
        }],
        "description": description,
        "mime_type": "application/json",
        "name": name,
        "size": compute_size(fname),
        "created_time": now_datetime,
        "updated_time": now_datetime,
        "version": "1",
    }
    return request_data


def post_metadata(fname, name, base_url, description=""):
    request_data = _create_request_data(fname, name, description)
    objects_endpoint = urljoin(base_url, "ga4gh/drs/v1/objects")
    response = requests.post(
        objects_endpoint,
        headers={"Content-Type": "application/json"},
        data=json.dumps(request_data))

    response.raise_for_status()
    return response.content.decode("ascii").strip()
