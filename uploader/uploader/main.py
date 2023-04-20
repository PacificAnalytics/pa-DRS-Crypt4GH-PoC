import argparse
import json
import requests
from urllib.parse import urljoin


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Upload file data and register metadata with Data Repository "
            "Service (DRS) web services")
    )
    parser.add_argument("name", type=str, help="File to upload")
    parser.add_argument(
        "--url", type=str, help="DRS base URL",
        default="http://localhost:8080"
    )
    parser.add_argument(
        "--desc", type=str, help="description of the object.", default="",
    )
    args = parser.parse_args()
    return args


def create_request_data(name, description):
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
        "created_time": "2023-04-17T12:16:16.957Z",
        "description": description,
        "mime_type": "application/json",
        "name": name,
        "size": 0,
        "updated_time": "2023-04-17T12:16:16.957Z",
        "version": "string",
    }
    return request_data


def main():
    args = parse_args()

    request_data = create_request_data(args.name, args.desc)
    objects_endpoint = urljoin(args.url, "ga4gh/drs/v1/objects")
    response = requests.post(
        objects_endpoint,
        headers={"Content-Type": "application/json"},
        data=json.dumps(request_data))

    response.raise_for_status()
    print(response.content.decode("ascii").strip())


if __name__ == "__main__":
    main()
