"""Main CLI entry point and command dispatcher for ngxctl."""

import sys
import click

from ngxctl import __version__
from ngxctl.commands.backup import backup_group
from ngxctl.commands.create import create_group
from ngxctl.commands.inspect import inspect_cmd, list_cmd
from ngxctl.commands.manage import (
    disable_cmd,
    enable_cmd,
    reload_cmd,
    restart_cmd,
    test_cmd,
)
from ngxctl.config import AppConfig


@click.group(invoke_without_command=False)
@click.version_option(version=__version__, prog_name="ngxctl")
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Enable verbose logging output.",
)
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """ngxctl - Command-line tool for generating, managing, and validating Nginx configurations."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["config"] = AppConfig.load()


# Register subcommands and command groups
cli.add_command(create_group)
cli.add_command(enable_cmd)
cli.add_command(disable_cmd)
cli.add_command(test_cmd)
cli.add_command(reload_cmd)
cli.add_command(restart_cmd)
cli.add_command(list_cmd)
cli.add_command(inspect_cmd)
cli.add_command(backup_group)


def main() -> None:
    """Execution wrapper for package scripts."""
    try:
        cli(obj={})
    except Exception as err:
        click.echo(f"Error: {err}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()