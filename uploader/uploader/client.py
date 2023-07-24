"""Easy (unified) access to the upload/download client.
"""
import os
import subprocess

import click
import yaml

DEFAULT_CONFIG_FILE = "drs-client.yaml"


class _ConfigManager:

    def __init__(self, data, fname):
        self.data = data
        self.fname = fname

    @classmethod
    def from_file(cls, fname):
        try:
            with open(fname, "rt", encoding="utf-8") as fp:
                data = yaml.safe_load(fp) or {}
        except FileNotFoundError:
            data = {}
        return cls(data, fname)

    def write_to_file(self):
        with open(self.fname, "wt", encoding="utf-8") as fp:
            yaml.dump(self.data, fp)

    def get(self, key):
        return self.data.get(key)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value


def _promptable_default_option(option, name, **kwds):

    class _OptionDefaultFromConfig(click.Option):

        def get_default(self, ctx, *args, **kwds):
            value = ctx.obj.get(name)
            return value or super().get_default(ctx, *args, **kwds)

    kwds = {
        "prompt": True,
        **kwds
    }
    return click.option(option, cls=_OptionDefaultFromConfig, **kwds)


def _parse_pk_file(fname):
    with open(fname, "rt", encoding="utf-8") as fp:
        return fp.readlines()[1].strip()


@click.option("-c", "--config", default=DEFAULT_CONFIG_FILE,
              help="Location of the configuration file")
@click.group()
@click.pass_context
def cli(ctx, config):
    ctx.obj = _ConfigManager.from_file(config)


# Decorators must appear in *reverse* order of how we want the prompts to
# appear to the user.
@_promptable_default_option("--secret-key", "secret_key",
                            prompt="Secret key for storage bucket")
@_promptable_default_option("--access-key", "access_key",
                            prompt="Access key (ID) for storage bucket")
@_promptable_default_option("--insecure", "insecure", is_flag=True,
                            prompt="Skip verification of TLS certificate?")
@_promptable_default_option("--bucket", "bucket",
                            prompt="Storage bucket")
@_promptable_default_option("--storage-url", "storage_url",
                            prompt="URL of the storage service (usually s3)")
@_promptable_default_option("--drs-url", "drs_url",
                            prompt="URL of the DRS server")
@click.command()
@click.pass_context
def configure(
        ctx, drs_url, storage_url, bucket, insecure, access_key, secret_key):
    """Configure the application settings."""
    cfg = ctx.obj
    cfg["drs_url"] = drs_url
    cfg["storage_url"] = storage_url
    cfg["bucket"] = bucket
    cfg["insecure"] = insecure
    cfg["access_key"] = access_key
    cfg["secret_key"] = secret_key

    cfg.write_to_file()
    click.echo(f"Configuration options written to {cfg.fname}")


@click.argument("filename", type=click.Path(exists=True))
@click.option("--client-sk",
              help="Secret key of the client",
              required=True)
@click.command()
@click.pass_context
def upload(ctx, filename, client_sk):
    """Upload a file to the server."""
    cfg = ctx.obj
    command = [
        "drs-uploader",
        filename,
        "--drs-url", cfg["drs_url"],
        "--storage-url", cfg["storage_url"],
        "--bucket", cfg["bucket"],
        "--encrypt",  # always encrypt
        "--client-sk", client_sk
    ]
    if cfg["insecure"]:
        command += ["--insecure"]
    os.environ.update({
        "ACCESS_KEY": cfg["access_key"],
        "SECRET_KEY": cfg["secret_key"],
    })

    subprocess.run(command, check=True)


@click.argument("drs-id")
@click.option("--recipient-pk",
              help="Public key of the third-party recipient",
              required=True)
@click.command()
@click.pass_context
def download(ctx, drs_id, recipient_pk):
    """Get a file from the server."""

    pkdata = _parse_pk_file(recipient_pk)
    os.environ["CRYPT4GH_PUBKEY"] = pkdata

    cfg = ctx.obj
    command = [
        "drs", "get", "-d",
        cfg["drs_url"],
        drs_id
    ]

    subprocess.run(command, check=True)


cli.add_command(configure)
cli.add_command(upload)
cli.add_command(download)


if __name__ == "__main__":
    cli()
