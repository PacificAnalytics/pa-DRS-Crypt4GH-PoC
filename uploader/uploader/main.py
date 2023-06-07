from pathlib import Path
import click

from .crypt4gh_client import get_server_pubkey
from .crypt4gh_wrapper import encrypt as _encrypt, get_seckey
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
@click.option("--encrypt", help="Encrypt file prior to upload", is_flag=True)
@click.option("--client-sk", help="Secret key of the client")
def main(filename, drs_url, storage_url, bucket, insecure, desc,
         encrypt, client_sk):
    """ Upload DRS metatadata and file byte data.
    """
    configure_logging()

    drs_client = DRSClient(drs_url)
    # Encrypt byte data
    if encrypt:
        server_pubkey, client_seckey = _load_crypt4gh_keys(
            drs_client, client_sk)
        filename = _encrypt_crypt4gh_file(
            filename, client_seckey, server_pubkey)

    # Upload byte data to storage server
    store_client = BucketStore(
        storage_url, bucket, secure=not insecure)
    resource_url = store_client.upload_file(filename)

    # Upload metadata to DRS-filer
    metadata = DRSMetadata.from_file(
        filename, url=resource_url, description=desc)

    meta_id = drs_client.post_metadata(metadata)
    print(meta_id)


def _load_crypt4gh_keys(client, client_sk):
    """Load crypt4gh key data, or bail out if a problem occurred."""
    server_pubkey = get_server_pubkey(client)
    if not server_pubkey:
        raise click.ClickException(
            "Encryption requested but server does not "
            "advertise a Crypt4gh public key.")

    client_seckey = get_seckey(client_sk)
    if not client_seckey:
        raise click.ClickException(
            f"Could not load client secret key from location: {client_sk}."
            " Specify a valid key with the --client-sk flag.")

    return server_pubkey, client_seckey


def _encrypt_crypt4gh_file(filename, client_seckey, server_pubkey):
    """Encrypt file with given server/client keys."""
    filename = Path(filename)
    filename_enc = filename.with_suffix(filename.suffix + ".crypt4gh")
    with open(filename, "rb") as orig, open(filename_enc, "wb") as enc:
        _encrypt(client_seckey, server_pubkey, orig, enc)
    return filename_enc


if __name__ == "__main__":
    main()
