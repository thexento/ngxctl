"""Core business logic engine for ngxctl."""

from ngxctl.core.backup import create_backup, list_backups, restore_backup
from ngxctl.core.generator import ConfigGenerator, SiteContext
from ngxctl.core.inspector import SiteInfo, get_site_info, list_all_sites
from ngxctl.core.system import (
    CommandResult,
    disable_site,
    enable_site,
    reload_nginx,
    restart_nginx,
    test_config,
)

__all__ = (
    "ConfigGenerator",
    "SiteContext",
    "CommandResult",
    "test_config",
    "reload_nginx",
    "restart_nginx",
    "enable_site",
    "disable_site",
    "create_backup",
    "list_backups",
    "restore_backup",
    "SiteInfo",
    "get_site_info",
    "list_all_sites",
)