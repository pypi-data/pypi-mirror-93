import textwrap

import click
from packaging.version import parse as parse_version

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError

from . import __version__


packages = {"notebook": "0.0", "pandas": "1.0", "matplotlib": "0.0", "lmfit": "0.0"}


@click.command()
@click.version_option(version=__version__)
def main():
    """Command-line interface providing tools for amsphyslab students and staff."""

    click.echo("Checking package versions...\n")

    is_env_ok = True
    for pkg, pkg_version in packages.items():
        try:
            version_ = version(pkg)
        except PackageNotFoundError:
            version_ = "Not installed"

        if parse_version(version_) < parse_version(pkg_version):
            if version_ == "Not installed":
                status = ""
            else:
                status = "insufficient"
            color = "red"
            is_env_ok = False
        else:
            status = "ok"
            color = "green"

        click.secho(f"{pkg:20s}\t{version_}\t{status}", fg=color, bold=True)

    if is_env_ok:
        click.secho("\nYou're environment seems to be in working order.")
    else:
        click.secho(
            textwrap.dedent(
                """
                You're environment is not suitable for our lab. You can try the following, at your own risk:

                    $ conda install anaconda=2020.11
                    $ conda install -c defaults -c conda-forge lmfit

                Or, a better solution:

                    $ conda create -n nsp1 notebook pandas matplotlib lmfit -c conda-forge
            
                And then each time you want to use this environment, use:

                    $ conda activate nsp1
                """
            )
        )
