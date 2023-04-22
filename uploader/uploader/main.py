import argparse

from .drs import DRSClient, DRSMetadata
from .store import BucketStore


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


def main():
    args = parse_args()

    # Upload byte data to storage server
    store_client = BucketStore("localhost:9000", "mybucket", secure=False)
    resource_url = store_client.upload_file(args.name)

    # Upload metadata to DRS-filer
    metadata = DRSMetadata.from_file(
        args.name, url=resource_url, description=args.desc)
    drs_client = DRSClient(args.url)
    meta_id = drs_client.post_metadata(metadata)
    print(meta_id)


if __name__ == "__main__":
    main()
