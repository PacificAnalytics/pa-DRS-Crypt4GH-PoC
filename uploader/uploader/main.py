import click

from .drs import DRSClient, DRSMetadata
from .store import BucketStore


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--drs-url", help="DRS-filer base URL", required=True)
@click.option("--storage-url", help="Storage backend", required=True)
@click.option("--bucket", help="Storage bucket", required=True)
@click.option("--insecure", help="Connect to storage insecurely", is_flag=True)
@click.option("--desc", help="Optional description of the object", default="")
def main(filename, drs_url, storage_url, bucket, insecure, desc):
    """ Upload DRS metatadata and file byte data.
    """

    # Encrypt byte data
    # ...

    # Upload byte data to storage server
    store_client = BucketStore(
        storage_url, bucket, secure=not insecure)
    resource_url = store_client.upload_file(filename)

    # Upload metadata to DRS-filer
    metadata = DRSMetadata.from_file(
        filename, url=resource_url, description=desc)
    drs_client = DRSClient(drs_url)
    meta_id = drs_client.post_metadata(metadata)
    print(meta_id)


if __name__ == "__main__":
    main()
