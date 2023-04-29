""" DRS metadata request handling.
"""
from dataclasses import dataclass
import datetime
import json
import logging
import os
from urllib.parse import urljoin

import requests

from .files import compute_sha256, compute_size

logger = logging.getLogger(__name__)


@dataclass
class DRSMetadata:
    """ Simple DRS object wrapper.

    Exposes just as many DRS attributes as are needed to register
    a simple object; more may be exposed in the future if needed.

    """
    name: str  # The name of the object, used to identify it
    checksum: str  # SHA-256 checksum
    size: int  # Size, in bytes
    url: str = ""  # URL to retrieve bytes
    description: str = ""  # Optional description

    @classmethod
    def from_file(cls, fpath, url="", description=""):
        """ Initialize a DRSMetadata object from a file.

        Parameters
        ----------
        fpath : str
            The file to take metadata from.
        url : str, optional
            URL with file byte data.
        description : str, optional
            An optional free-form description.

        """
        return cls(
            name=os.path.basename(fpath),
            checksum=compute_sha256(fpath),
            size=compute_size(fpath),
            url=url,
            description=description,
        )


class DRSClient:
    """ Thin client for DRS-filer object uploading.

    The client currently only supports uploading of single objects, not
    of bundles. As the DRS API is read-only, it uses the (custom) POST
    endpoint that DRS-filer exposes to upload object data.

    """

    def __init__(self, drs_url):
        self._drs_url = drs_url

    def post_metadata(self, drs_metadata):
        """ Upload a single metadata object.

        Parameters
        ----------
        drs_metadata : DRSMetadata
            DRS metadata object to be uploaded.

        """
        request_data = _create_request_data(drs_metadata)
        objects_endpoint = urljoin(self._drs_url, "ga4gh/drs/v1/objects")

        logger.debug("Uploading metadata %s to %s",
                     drs_metadata, objects_endpoint)

        response = requests.post(
            objects_endpoint,
            headers={"Content-Type": "application/json"},
            data=json.dumps(request_data))

        response.raise_for_status()
        object_id = response.content.decode("ascii").strip()

        logger.debug("Upload complete for object ID %s", object_id)

        return object_id

    def get_service_info(self):
        service_info = urljoin(self._drs_url, "ga4gh/drs/v1/service-info")

        response = requests.get(service_info)
        response.raise_for_status()

        return response.json()


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
