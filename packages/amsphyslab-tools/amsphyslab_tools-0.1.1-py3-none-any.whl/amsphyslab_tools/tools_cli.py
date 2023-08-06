import click

from . import __version__


@click.command()
@click.version_option(version=__version__)
def main():
    """Command-line interface providing tools for amsphyslab students and staff."""
    click.echo("Hello, world.")
