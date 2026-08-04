"""Main CLI entry point and command registration for ngxctl."""

import sys
import click

from ngxctl import __version__
from ngxctl.config import AppConfig


@click.group(invoke_without_command=False)
@click.version_option(version=__version__, prog_name="ngxctl")
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Enable verbose output for debugging.",
)
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """ngxctl - Command-line tool for generating and managing Nginx configurations."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["config"] = AppConfig.load()


def main() -> None:
    """Entry point wrapper for setuptools script execution."""
    try:
        cli(obj={})
    except Exception as err:
        click.echo(f"Error: {err}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()