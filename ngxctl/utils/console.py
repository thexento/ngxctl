"""Console output formatting and terminal helper functions for ngxctl."""

import click


def info(message: str) -> None:
    """Print an informational message to stdout."""
    prefix = click.style("[i]", fg="blue", bold=True)
    click.echo(f"{prefix} {message}")


def success(message: str) -> None:
    """Print a success message to stdout."""
    prefix = click.style("[✓]", fg="green", bold=True)
    click.echo(f"{prefix} {message}")


def warning(message: str) -> None:
    """Print a warning message to stdout."""
    prefix = click.style("[!]", fg="yellow", bold=True)
    click.echo(f"{prefix} {message}")


def error(message: str) -> None:
    """Print an error message to stderr."""
    prefix = click.style("[✗]", fg="red", bold=True)
    click.echo(f"{prefix} {message}", err=True)


def confirm(prompt_text: str, default: bool = False) -> bool:
    """Prompt the user for yes/no confirmation.
    
    Returns True if confirmed, False otherwise.
    """
    return click.confirm(prompt_text, default=default)