"""Nginx service management, validation, and site link administration."""

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from ngxctl.config import NginxPaths
from ngxctl.utils.fs import create_symlink, is_root, remove_path


@dataclass(frozen=True, slots=True)
class CommandResult:
    """Result of an executed external process command."""

    success: bool
    returncode: int
    stdout: str
    stderr: str


def test_config(nginx_binary: str = "nginx") -> CommandResult:
    """Validate Nginx configuration syntax using `nginx -t`."""
    binary_path = shutil.which(nginx_binary)
    if not binary_path:
        return CommandResult(
            success=False,
            returncode=127,
            stdout="",
            stderr=f"Executable '{nginx_binary}' not found in system PATH.",
        )

    proc = subprocess.run(
        [binary_path, "-t"],
        capture_output=True,
        text=True,
        check=False,
    )

    return CommandResult(
        success=(proc.returncode == 0),
        returncode=proc.returncode,
        stdout=proc.stdout.strip(),
        stderr=proc.stderr.strip(),
    )


def reload_nginx(nginx_binary: str = "nginx") -> CommandResult:
    """Reload Nginx configuration without dropping active connections."""
    systemctl_path = shutil.which("systemctl")

    # Try systemd service reload if available
    if systemctl_path:
        proc = subprocess.run(
            [systemctl_path, "reload", "nginx"],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0:
            return CommandResult(
                success=True,
                returncode=0,
                stdout=proc.stdout.strip(),
                stderr=proc.stderr.strip(),
            )

    # Fallback to direct `nginx -s reload` binary call
    binary_path = shutil.which(nginx_binary)
    if not binary_path:
        return CommandResult(
            success=False,
            returncode=127,
            stdout="",
            stderr="Neither 'systemctl' nor 'nginx' binary was found in PATH.",
        )

    proc = subprocess.run(
        [binary_path, "-s", "reload"],
        capture_output=True,
        text=True,
        check=False,
    )

    return CommandResult(
        success=(proc.returncode == 0),
        returncode=proc.returncode,
        stdout=proc.stdout.strip(),
        stderr=proc.stderr.strip(),
    )


def restart_nginx(nginx_binary: str = "nginx") -> CommandResult:
    """Restart Nginx service."""
    systemctl_path = shutil.which("systemctl")

    if systemctl_path:
        proc = subprocess.run(
            [systemctl_path, "restart", "nginx"],
            capture_output=True,
            text=True,
            check=False,
        )
        return CommandResult(
            success=(proc.returncode == 0),
            returncode=proc.returncode,
            stdout=proc.stdout.strip(),
            stderr=proc.stderr.strip(),
        )

    return reload_nginx(nginx_binary)


def enable_site(site_name: str, paths: NginxPaths) -> Path:
    """Enable a site configuration by symlinking sites-available to sites-enabled.
    
    Raises FileNotFoundError if the source file in sites-available does not exist.
    """
    if not paths.uses_sites_structure or not paths.sites_available or not paths.sites_enabled:
        raise ValueError(
            "This Nginx setup does not use sites-available / sites-enabled structure."
        )

    config_filename = f"{site_name}.conf" if not site_name.endswith(".conf") else site_name
    source_path = paths.sites_available / config_filename
    target_path = paths.sites_enabled / config_filename

    if not source_path.exists():
        # Check without .conf extension fallback
        alt_source = paths.sites_available / site_name
        if alt_source.exists():
            source_path = alt_source
            target_path = paths.sites_enabled / site_name
        else:
            raise FileNotFoundError(
                f"Configuration file for '{site_name}' not found in {paths.sites_available}"
            )

    create_symlink(source_path, target_path, force=True)
    return target_path


def disable_site(site_name: str, paths: NginxPaths) -> bool:
    """Disable a site configuration by removing its symlink from sites-enabled.
    
    Returns True if disabled successfully, False if site was not currently enabled.
    """
    if not paths.uses_sites_structure or not paths.sites_enabled:
        raise ValueError(
            "This Nginx setup does not use sites-available / sites-enabled structure."
        )

    config_filename = f"{site_name}.conf" if not site_name.endswith(".conf") else site_name
    target_path = paths.sites_enabled / config_filename

    if not target_path.exists() and not target_path.is_symlink():
        alt_target = paths.sites_enabled / site_name
        if alt_target.exists() or alt_target.is_symlink():
            target_path = alt_target

    return remove_path(target_path)