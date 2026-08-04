"""Command modules and CLI handlers for ngxctl."""

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

__all__ = (
    "create_group",
    "backup_group",
    "enable_cmd",
    "disable_cmd",
    "test_cmd",
    "reload_cmd",
    "restart_cmd",
    "list_cmd",
    "inspect_cmd",
)