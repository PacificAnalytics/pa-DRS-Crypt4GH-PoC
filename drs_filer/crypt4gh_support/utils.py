"""Supporting code for crypt4gh module."""

from contextlib import contextmanager
from pathlib import Path
import tempfile
import shutil
import uuid


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
