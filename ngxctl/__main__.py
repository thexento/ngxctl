"""Execution entrypoint for ngxctl when invoked as a module (`python -m ngxctl`)."""

import sys
from ngxctl.cli import cli


def main() -> None:
    """Run the ngxctl CLI application."""
    cli()


if __name__ == "__main__":
    main()