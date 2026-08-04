"""Configuration settings and path resolution logic for ngxctl."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Final

# Environment variable keys
ENV_NGINX_DIR: Final[str] = "NGXCTL_NGINX_DIR"
ENV_SITES_AVAILABLE: Final[str] = "NGXCTL_SITES_AVAILABLE"
ENV_SITES_ENABLED: Final[str] = "NGXCTL_SITES_ENABLED"
ENV_CONF_D: Final[str] = "NGXCTL_CONF_D"
ENV_BACKUP_DIR: Final[str] = "NGXCTL_BACKUP_DIR"

# Standard system search locations
DEBIAN_AVAILABLE: Final[Path] = Path("/etc/nginx/sites-available")
DEBIAN_ENABLED: Final[Path] = Path("/etc/nginx/sites-enabled")
RHEL_CONF_D: Final[Path] = Path("/etc/nginx/conf.d")

HOMEBREW_ARM_NGINX: Final[Path] = Path("/opt/homebrew/etc/nginx")
HOMEBREW_INTEL_NGINX: Final[Path] = Path("/usr/local/etc/nginx")


@dataclass(frozen=True, slots=True)
class NginxPaths:
    """Resolved Nginx directory paths on the target system."""

    nginx_dir: Path
    sites_available: Path | None
    sites_enabled: Path | None
    conf_d: Path | None
    uses_sites_structure: bool

    @classmethod
    def detect(cls) -> "NginxPaths":
        """Detect and resolve active Nginx configuration paths."""
        # Check explicit environment variable overrides
        env_nginx = os.getenv(ENV_NGINX_DIR)
        nginx_dir = Path(env_nginx) if env_nginx else Path("/etc/nginx")

        env_available = os.getenv(ENV_SITES_AVAILABLE)
        env_enabled = os.getenv(ENV_SITES_ENABLED)
        env_conf_d = os.getenv(ENV_CONF_D)

        # 1. Environment variables set explicitly
        if env_available and env_enabled:
            return cls(
                nginx_dir=nginx_dir,
                sites_available=Path(env_available),
                sites_enabled=Path(env_enabled),
                conf_d=Path(env_conf_d) if env_conf_d else None,
                uses_sites_structure=True,
            )

        # 2. Debian/Ubuntu structure (sites-available / sites-enabled)
        if DEBIAN_AVAILABLE.exists() and DEBIAN_ENABLED.exists():
            return cls(
                nginx_dir=DEBIAN_AVAILABLE.parent,
                sites_available=DEBIAN_AVAILABLE,
                sites_enabled=DEBIAN_ENABLED,
                conf_d=RHEL_CONF_D if RHEL_CONF_D.exists() else None,
                uses_sites_structure=True,
            )

        # 3. macOS Homebrew ARM (/opt/homebrew/etc/nginx)
        if HOMEBREW_ARM_NGINX.exists():
            brew_conf_d = HOMEBREW_ARM_NGINX / "servers"
            return cls(
                nginx_dir=HOMEBREW_ARM_NGINX,
                sites_available=None,
                sites_enabled=None,
                conf_d=brew_conf_d if brew_conf_d.exists() else HOMEBREW_ARM_NGINX,
                uses_sites_structure=False,
            )

        # 4. macOS Homebrew Intel (/usr/local/etc/nginx)
        if HOMEBREW_INTEL_NGINX.exists():
            brew_conf_d = HOMEBREW_INTEL_NGINX / "servers"
            return cls(
                nginx_dir=HOMEBREW_INTEL_NGINX,
                sites_available=None,
                sites_enabled=None,
                conf_d=brew_conf_d if brew_conf_d.exists() else HOMEBREW_INTEL_NGINX,
                uses_sites_structure=False,
            )

        # 5. RHEL / CentOS / Arch / Alpine fallback (conf.d)
        if RHEL_CONF_D.exists():
            return cls(
                nginx_dir=RHEL_CONF_D.parent,
                sites_available=None,
                sites_enabled=None,
                conf_d=RHEL_CONF_D,
                uses_sites_structure=False,
            )

        # 6. Default fallback to Debian standard paths
        return cls(
            nginx_dir=nginx_dir,
            sites_available=DEBIAN_AVAILABLE,
            sites_enabled=DEBIAN_ENABLED,
            conf_d=None,
            uses_sites_structure=True,
        )


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Global configuration object for ngxctl."""

    nginx_paths: NginxPaths
    user_config_dir: Path
    backup_dir: Path
    user_templates_dir: Path

    @classmethod
    def load(cls) -> "AppConfig":
        """Load and resolve application configuration."""
        home = Path.home()
        config_root = home / ".config" / "ngxctl"

        env_backup = os.getenv(ENV_BACKUP_DIR)
        backup_dir = Path(env_backup) if env_backup else config_root / "backups"
        templates_dir = config_root / "templates"

        return cls(
            nginx_paths=NginxPaths.detect(),
            user_config_dir=config_root,
            backup_dir=backup_dir,
            user_templates_dir=templates_dir,
        )