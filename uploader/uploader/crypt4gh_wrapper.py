""" Convenience wrappers around common crypt4gh functionality.
"""
from base64 import b64decode, b64encode
from pathlib import Path

from crypt4gh.keys import get_private_key, get_public_key
from crypt4gh.lib import encrypt as _encrypt, reencrypt as _reencrypt


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
    filename_enc : Path
        Filename of the encrypted file.

    """
    filename = Path(filename)
    filename_enc = filename.with_suffix(filename.suffix + extension)

    recipients = [(0, client_seckey, recipient_pubkey)]
    with open(filename, "rb") as fp_in, open(filename_enc, "wb") as fp_out:
        _encrypt(recipients, fp_in, fp_out, 0, None)

    return filename_enc


def reencrypt(owner_seckey, recipient_pubkey, filename, extension=".reenc"):
    """ Reencrypts a crypt4gh file for a new recipient.

    Parameters
    ----------
    owner_seckey : bytes
        Crypt4gh private key of the owner of the file.
    recipient_pubkey : bytes
        Crypt4gh public key of the recipient.

    Returns
    -------
    filename_reenc : Path
        Filename of the re-encrypted file.

    """
    filename = Path(filename)
    filename_reenc = filename.with_suffix(filename.suffix + extension)

    recipients = [(0, owner_seckey, recipient_pubkey)]
    with open(filename, "rb") as fp_in, open(filename_reenc, "wb") as fp_out:
        _reencrypt([(0, owner_seckey, None)], recipients, fp_in, fp_out)

    return filename_reenc


def get_seckey(filepath):
    """ Load private key from file.

    Assumes that the key does not have a passphrase.

    """
    return get_private_key(filepath, lambda: "")


def get_pubkey(filepath):
    """ Load public key from file.

    Simply calls through to crypt4gh implementation.

    Returns
    -------
    key : bytes
    """
    return get_public_key(filepath)


def get_pubkey_b64(filepath):
    """ Load public key from file.

    Returns
    -------
    b64_key : str
        Base-64 encoded public key.
    """
    return b64encode(get_pubkey(filepath)).decode("ascii")


def get_key_from_bytes(key):
    """ Decode b64-encoded key.
    """
    return b64decode(key)
