"""Convenience wrappers around common crypt4gh functionality."""
from base64 import b64encode

from crypt4gh.keys import get_public_key


def get_pubkey(filepath):
    """Load public key from file.

    Simply calls through to crypt4gh implementation.

    Returns:
        Key as bytes.

    """
    return get_public_key(filepath)


def get_pubkey_b64(filepath):
    """Load public key from file.

    Returns:
        Base-64 encoded public key.

    """
    return b64encode(get_pubkey(filepath)).decode("ascii")
