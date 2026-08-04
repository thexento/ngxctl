"""Utility functions and terminal formatting helpers for ngxctl."""

from ngxctl.utils.console import confirm, error, info, success, warning
from ngxctl.utils.fs import (
    atomic_write,
    can_write,
    create_symlink,
    ensure_directory,
    is_root,
    remove_path,
)

__all__ = (
    "is_root",
    "can_write",
    "ensure_directory",
    "atomic_write",
    "create_symlink",
    "remove_path",
    "info",
    "success",
    "warning",
    "error",
    "confirm",
)