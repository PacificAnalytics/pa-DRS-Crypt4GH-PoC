"""Easy (unified) access to the upload/download client.
"""

import click

@click.group()
def cli():
    pass


@click.command()
def configure():
    """Configure the application settings."""
    click.echo("Configuring...")


@click.command()
def upload():
    """Upload a file to the server."""
    click.echo("Uploading...")


@click.command()
def get():
    """Get a file from the server."""
    click.echo("Getting...")


cli.add_command(configure)
cli.add_command(upload)
cli.add_command(get)


if __name__ == "__main__":
    cli()
