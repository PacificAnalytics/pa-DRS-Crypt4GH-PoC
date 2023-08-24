import os
from unittest.mock import patch

from drs_filer.crypt4gh_support.config import Crypt4GHConfig


def test_config_environment():
    """Test that environment variables take precendence."""
    env = {
        "PUBKEY_PATH": "/a/b/c",
        "SECKEY_PATH": "/d/e/f",
        "STORAGE_HOST": "localhost:9999",
        "STORAGE_BUCKET": "mybucket",
    }
    with patch.dict(os.environ, env):
        c = Crypt4GHConfig(
            pubkey_path="X", seckey_path="Y", storage_host="Z",
            storage_bucket="U"
        )

    assert c.pubkey_path == env["PUBKEY_PATH"]
    assert c.seckey_path == env["SECKEY_PATH"]
    assert c.storage_host == env["STORAGE_HOST"]
    assert c.storage_bucket == env["STORAGE_BUCKET"]
