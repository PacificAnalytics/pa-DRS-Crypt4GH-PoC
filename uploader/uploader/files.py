import hashlib
import os


def compute_sha256(fname):
    """ Compute SHA-256 checksum of file contents.
    """
    m = hashlib.sha256()
    with open(fname, 'rb') as fp:
        m.update(fp.read())
    return m.hexdigest()


def compute_size(fname):
    """ Compute size (in bytes) of file.
    """
    return os.stat(fname).st_size
