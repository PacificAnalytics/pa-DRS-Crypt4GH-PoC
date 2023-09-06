"""Convenience wrappers around common crypt4gh functionality."""
from base64 import b64encode

from crypt4gh.keys import get_private_key, get_public_key
from crypt4gh.lib import reencrypt as _reencrypt


class EncryptionError(Exception):
    """Generic exception to raise upon (re)encryption error."""


def reencrypt(server_seckey, recipient_pubkey, encrypted_fp, reencrypted_fp):
    """Reencrypts a crypt4gh file for a new recipient.

    Args:
        server_seckey (bytes): Crypt4gh private key (of the server).
        recipient_pubkey (bytes): Crypt4gh public key of the recipient.
        encrypted_fp: File handle for file data (opened for reading).
        reencrypted_fp: File handle to write re-encrypted data to.

    """
    keys = [(0, server_seckey, None)]
    recipients = [(0, server_seckey, recipient_pubkey)]
    try:
        _reencrypt(keys, recipients, encrypted_fp, reencrypted_fp)
    except Exception as e:
        raise EncryptionError() from e


def get_seckey(filepath):
    """Load private key from file.

    Assumes that the key does not have a passphrase.

    """
    return get_private_key(filepath, lambda: "")


def get_pubkey(filepath):
    """Load public key from file.

    Simply calls through to crypt4gh implementation.

    Returns:
        key (bytes)
    """
    return get_public_key(filepath)


def get_pubkey_b64(filepath):
    """Load public key from file.

    Returns:
        b64_key (str): Base-64 encoded public key.
    """
    return b64encode(get_pubkey(filepath)).decode("ascii")
