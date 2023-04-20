from ..files import compute_sha256
from .testing_utils import datafile


def test_compute_sha256():
    with datafile("test file data") as fname:
        assert compute_sha256(fname) == "1be7aaf1938cc19af7d2fdeb48a11c381dff8a98d4c4b47b3b0a5044a5255c04"  # noqa
