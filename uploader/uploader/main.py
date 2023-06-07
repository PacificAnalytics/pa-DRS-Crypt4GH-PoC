from pathlib import Path

import click

from .crypt4gh_client import get_server_pubkey
from .crypt4gh_wrapper import encrypt, get_seckey
from .drs import DRSClient, DRSMetadata
from .store import BucketStore
from .utils import configure_logging


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--drs-url", help="DRS-filer base URL", required=True)
@click.option("--storage-url", help="Storage backend", required=True)
@click.option("--bucket", help="Storage bucket", required=True)
@click.option("--insecure", help="Connect to storage insecurely", is_flag=True)
@click.option("--desc", help="Optional description of the object", default="")
@click.option("--sk", help="Secret key of the client", required=True)
def main(filename, drs_url, storage_url, bucket, insecure, desc, sk):
    """Upload DRS metatadata and file byte data."""
    configure_logging()

    # Encrypt byte data
    drs_client = DRSClient(drs_url)
    server_pubkey = get_server_pubkey(drs_client)
    if server_pubkey:  # supports crypt4gh
        client_seckey = get_seckey(sk)

        filename = Path(filename)
        filename_enc = filename.with_suffix(filename.suffix + ".crypt4gh")
        with open(filename, "rb") as orig, open(filename_enc, "wb") as enc:
            encrypt(client_seckey, server_pubkey, orig, enc)

    # Upload byte data to storage server
    store_client = BucketStore(
        storage_url, bucket, secure=not insecure)
    resource_url = store_client.upload_file(filename)

    # Upload metadata to DRS-filer
    metadata = DRSMetadata.from_file(
        filename, url=resource_url, description=desc)
    meta_id = drs_client.post_metadata(metadata)
    print(meta_id)


if __name__ == "__main__":
    main()
