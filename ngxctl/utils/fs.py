"""Safe filesystem utility functions and privilege management for ngxctl."""

import os
import sys
import tempfile
from pathlib import Path
import click

from ngxctl.utils import console


def is_root() -> bool:
    """Check if the current process has root privileges (EUID == 0)."""
    return hasattr(os, "geteuid") and os.geteuid() == 0


def can_write(path: Path) -> bool:
    """Check if the current process has write access to a directory or file path."""
    target = path if path.exists() else path.parent
    return os.access(target, os.W_OK)


def elevate_privileges() -> None:
    """Re-executes the current ngxctl CLI invocation with sudo while preserving PYTHONPATH."""
    if not is_root():
        # Preserve user's Python module search path so root's Python can import ngxctl
        python_path = os.pathsep.join(sys.path)
        args = ["sudo", "env", f"PYTHONPATH={python_path}", sys.executable] + sys.argv
        os.execvp("sudo", args)


def check_root_or_elevate(action_description: str = "file operations in /etc/nginx", auto_prompt: bool = True) -> bool:
    """Check for root privileges. If missing, warn user and offer auto-elevation.
    
    Returns True if running as root or after successful elevation.
    """
    if is_root():
        return True

    console.warning(f"ngxctl does not have root/sudo permissions to perform {action_description}.")
    
    command_str = " ".join(sys.argv)
    click.echo(f"    To run manually: {click.style(f'sudo {command_str}', fg='cyan', bold=True)}")

    if auto_prompt:
        if console.confirm("    Would you like ngxctl to elevate automatically using sudo now?", default=True):
            elevate_privileges()
            return True

    return False


def ensure_directory(path: Path) -> None:
    """Ensure that a directory path exists, creating parent directories if necessary."""
    path.mkdir(parents=True, exist_ok=True)


def atomic_write(target_path: Path, content: str) -> None:
    """Safely write content to a file atomically via a temporary file replacement."""
    ensure_directory(target_path.parent)

    temp_fd, temp_path_str = tempfile.mkstemp(
        dir=target_path.parent,
        prefix=f".{target_path.name}.tmp-",
    )
    temp_path = Path(temp_path_str)

    try:
        with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())

        os.replace(temp_path, target_path)
    except Exception:
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)
        raise


def create_symlink(source: Path, target: Path, force: bool = True) -> None:
    """Create a symbolic link from source to target."""
    ensure_directory(target.parent)

    if target.is_symlink() or target.exists():
        if force:
            target.unlink(missing_ok=True)
        else:
            raise FileExistsError(f"Target path already exists: {target}")

    target.symlink_to(source)


def remove_path(target: Path) -> bool:
    """Safely remove a file or symlink if it exists."""
    if target.is_symlink() or target.exists():
        target.unlink(missing_ok=True)
        return True
    return False