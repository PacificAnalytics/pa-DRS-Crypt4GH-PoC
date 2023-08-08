from pydantic import BaseSettings


class Crypt4GHConfig(BaseSettings):
    """Configuration for Crypt4GH-specific functionality.

    Configuration items can be passed in at init time, or
    as environment variables. The latter take precedence.

    """

    pubkey_path: str
    seckey_path: str
    storage_host: str
    storage_bucket: str

    class Config:

        @classmethod
        def customise_sources(cls,
                              init_settings,
                              env_settings,
                              file_secret_settings):
            """Allow environment variables to override other config items."""
            return env_settings, init_settings, file_secret_settings
