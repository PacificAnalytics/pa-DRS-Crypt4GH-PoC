""" Convenience wrappers around common crypt4gh functionality.
"""
from base64 import b64decode
from pathlib import Path

from crypt4gh.keys import get_private_key
from crypt4gh.lib import encrypt as _encrypt


def encrypt(client_seckey, recipient_pubkey, filename, extension=".crypt4gh"):
    """ Encrypt file for given recipient.

    Encrypted file is placed in the same directory as the original file.

    Parameters
    ----------
    client_seckey : bytes
        Crypt4gh private key of the client (owner of the file).
    recipient_pubkey : bytes
        Crypt4gh public key of the recipient.

    Returns
    -------
    filename_enc : str
        Filename of the encrypted file.

    """
    filename = Path(filename)
    filename_enc = filename.with_suffix(filename.suffix + extension)

    recipients = [(0, client_seckey, recipient_pubkey)]
    with open(filename, "rb") as fp_in, open(filename_enc, "wb") as fp_out:
        _encrypt(recipients, fp_in, fp_out, 0, None)

    return filename_enc


def get_seckey(filepath):
    """ Load private key from file.

    Assumes that the key does not have a passphrase.

    """
    return get_private_key(filepath, lambda: "")


def get_key_from_bytes(key):
    """ Decode b64-encoded key.
    """
    return b64decode(key)
