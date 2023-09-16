"""Supporting code for crypt4gh module."""

from base64 import b64encode
from contextlib import contextmanager
import os
from pathlib import Path
import tempfile
import shutil
import uuid

from crypt4gh_common import get_pubkey, get_seckey


@contextmanager
def temp_folder():
    """Create a temporary folder."""
    d = Path(tempfile.mkdtemp())
    try:
        yield d
    finally:
        shutil.rmtree(d)


def create_unique_filename(base_dir):
    """Create a unique filename relative to the given directory."""
    return Path(base_dir) / str(uuid.uuid4())


def get_pubkey_b64_from_env():
    """Read Crypt4GH public key from the environment.

    Looks for the ``PUB_KEY`` environment variable, which should contain a
    properly formatted Crypt4GH key.
    """
    try:
        pubkey = os.environ["PUB_KEY"]
    except KeyError:
        raise RuntimeError(
            "No server public key found. You can provide one by setting the "
            "environment variable PUB_KEY to contain a valid "
            "Crypt4GH key.") from None

    # TODO: We write the secret key to a temporary file to read it in again
    # with crypt4gh.keys.get_private_key, which expects a file path.
    with temp_folder() as d:
        filepath = d / "server.sk"
        with open(filepath, "wt", encoding="utf-8") as fp:
            fp.write(pubkey)
        pubkey_data = get_pubkey(filepath)
        pubkey_b64 = b64encode(pubkey_data).decode("ascii")

    return pubkey_b64


def get_seckey_from_env():
    """Load private key from the environment.

    Looks under the environment variable ``SEC_KEY``; assumes that the
    key is formatted in standard Crypt4GH format and does not have a
    passphrase.

    """
    try:
        seckey = os.environ["SEC_KEY"]
    except KeyError:
        raise RuntimeError(
            "No server secret key found. You can provide one by setting the "
            "environment variable SEC_KEY to contain a valid "
            "Crypt4GH key.") from None

    # TODO: We write the secret key to a temporary file to read it in again
    # with crypt4gh.keys.get_private_key, which expects a file path.
    with temp_folder() as d:
        filepath = d / "server.sk"
        with open(filepath, "wt", encoding="utf-8") as fp:
            fp.write(seckey)
        parsed_key = get_seckey(filepath)

    return parsed_key
