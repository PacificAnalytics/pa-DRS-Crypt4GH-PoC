""" DRS metadata request handling.
"""

import json
import requests
from urllib.parse import urljoin


def _create_request_data(name, description):
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
        "checksums": [{"checksum": "string", "type": "sha-256"}],
        "description": description,
        "mime_type": "application/json",
        "name": name,
        "size": 0,
        "created_time": "2023-04-17T12:16:16.957Z",
        "updated_time": "2023-04-17T12:16:16.957Z",
        "version": "string",
    }
    return request_data


def post_metadata(name, base_url, description=""):
    request_data = _create_request_data(name, description)
    objects_endpoint = urljoin(base_url, "ga4gh/drs/v1/objects")
    response = requests.post(
        objects_endpoint,
        headers={"Content-Type": "application/json"},
        data=json.dumps(request_data))

    response.raise_for_status()
    return response.content.decode("ascii").strip()
