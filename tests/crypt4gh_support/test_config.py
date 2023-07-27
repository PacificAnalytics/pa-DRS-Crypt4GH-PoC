import os
from unittest.mock import patch

from drs_filer.crypt4gh_support.config import Crypt4GHConfig


def test_config_environment():
    """Test that environment variables take precendence."""
    env = {
        "STORAGE_HOST": "localhost:9999",
        "STORAGE_BUCKET": "mybucket",
        "STORAGE_SECURE": "1",
    }
    with patch.dict(os.environ, env):
        c = Crypt4GHConfig(
            storage_host="Z",
            storage_bucket="U",
            storage_secure=False
        )

    assert c.storage_host == env["STORAGE_HOST"]
    assert c.storage_bucket == env["STORAGE_BUCKET"]
    assert c.storage_secure
