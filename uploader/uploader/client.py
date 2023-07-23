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

    return click.option(
        option, prompt=True, cls=_OptionDefaultFromConfig, **kwds
    )


def _parse_pk_file(fname):
    with open(fname, "rt", encoding="utf-8") as fp:
        return fp.readlines()[1]


@click.option("-c", "--config", default=DEFAULT_CONFIG_FILE,
              help="Location of the configuration file")
@click.group()
@click.pass_context
def cli(ctx, config):
    ctx.obj = _ConfigManager.from_file(config)


@_promptable_default_option("--drs-url", "drs_url")
@_promptable_default_option("--storage-url", "storage_url")
@_promptable_default_option("--bucket", "bucket")
@_promptable_default_option("--insecure", "insecure", is_flag=True)
@_promptable_default_option("--access-key", "access_key")
@_promptable_default_option("--secret-key", "secret_key")
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
@click.option("--client-sk", help="Secret key of the client")
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
@click.option("--receiver-pk", help="Public key of the third-party receiver")
@click.command()
@click.pass_context
def download(ctx, drs_id, receiver_pk):
    """Get a file from the server."""

    pkdata = _parse_pk_file(receiver_pk)
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
