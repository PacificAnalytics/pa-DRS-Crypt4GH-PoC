from typing import Optional

from pydantic import BaseModel


class Crypt4GHConfig(BaseModel):
    """Configuration for Crypt4GH-specific functionality."""

    pubkey_path: str
    seckey_path: str
    storage_host: str
    storage_bucket: str
    storage_secure: Optional[bool] = True
