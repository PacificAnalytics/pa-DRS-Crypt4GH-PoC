from ..crypt4gh_wrapper import get_pubkey_b64
from .testing_utils import datafile


PK = """\n
-----BEGIN CRYPT4GH PUBLIC KEY-----
AmEsb2n0m5mc6aadwpK4sT6zNapqgH+nnysNtpKa2Ag=
-----END CRYPT4GH PUBLIC KEY-----
"""


def test_get_pubkey_b64():
    with datafile(PK) as fname:
        assert get_pubkey_b64(fname) == "AmEsb2n0m5mc6aadwpK4sT6zNapqgH+nnysNtpKa2Ag="  # noqa
