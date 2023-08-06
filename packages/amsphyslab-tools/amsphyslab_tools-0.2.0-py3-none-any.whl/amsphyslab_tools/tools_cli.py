import click
from packaging.version import parse as parse_version
from rich.console import Console
from rich.table import Table

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError

from . import __version__


packages = {"notebook": "", "pandas": "1.0", "matplotlib": "", "lmfit": ""}


@click.command()
@click.version_option(version=__version__)
def main():
    """Command-line interface providing tools for amsphyslab students and staff."""

    console = Console()
    console.print("Checking package versions...\n")

    table = Table(box=None)
    table.add_column("Package", style="")
    table.add_column("Version", style="bold")
    table.add_column("", style="bold")

    for pkg, pkg_version in packages.items():
        try:
            version_ = version(pkg)
        except PackageNotFoundError:
            version_ = "Not installed"

        if version_ == "Not installed" or parse_version(version_) < parse_version(
            pkg_version
        ):
            status = "[red] insufficient"
        else:
            status = "[green] ok"

        table.add_row(pkg, f"{version_}", status)

    console.print(table)
