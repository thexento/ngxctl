"""Safe filesystem utility functions for ngxctl."""

import os
import tempfile
from pathlib import Path


def is_root() -> bool:
    """Check if the current process has root privileges (EUID == 0)."""
    return hasattr(os, "geteuid") and os.geteuid() == 0


def can_write(path: Path) -> bool:
    """Check if the current process has write access to a directory or file path."""
    target = path if path.exists() else path.parent
    return os.access(target, os.W_OK)


def ensure_directory(path: Path) -> None:
    """Ensure that a directory path exists, creating parent directories if necessary."""
    path.mkdir(parents=True, exist_ok=True)


def atomic_write(target_path: Path, content: str) -> None:
    """Safely write content to a file atomically via a temporary file replacement.
    
    Prevents corrupting active Nginx configurations if writing fails mid-operation.
    """
    ensure_directory(target_path.parent)

    # Create temporary file in the same target directory to ensure same filesystem mount for os.replace
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

        # Atomically replace target file
        os.replace(temp_path, target_path)
    except Exception:
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)
        raise


def create_symlink(source: Path, target: Path, force: bool = True) -> None:
    """Create a symbolic link from source to target.
    
    If force is True, overwrites an existing destination symlink or file.
    """
    ensure_directory(target.parent)

    if target.is_symlink() or target.exists():
        if force:
            target.unlink(missing_ok=True)
        else:
            raise FileExistsError(f"Target path already exists: {target}")

    target.symlink_to(source)


def remove_path(target: Path) -> bool:
    """Safely remove a file or symlink if it exists.
    
    Returns True if a path was removed, False if it did not exist.
    """
    if target.is_symlink() or target.exists():
        target.unlink(missing_ok=True)
        return True
    return False