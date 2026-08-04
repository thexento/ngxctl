"""Inspection and status discovery for active and available Nginx sites."""

import re
from dataclasses import dataclass, field
from pathlib import Path

from ngxctl.config import NginxPaths


@dataclass(frozen=True, slots=True)
class SiteInfo:
    """Metadata and operational status for an Nginx site configuration."""

    name: str
    available_path: Path | None
    enabled_path: Path | None
    is_enabled: bool
    domains: list[str] = field(default_factory=list)
    ports: list[int] = field(default_factory=list)
    has_ssl: bool = False
    is_proxy: bool = False


# Directive extraction regex patterns
RE_SERVER_NAME = re.compile(r"server_name\s+([^;]+);", re.IGNORECASE)
RE_LISTEN_PORT = re.compile(r"listen\s+(?:\[::\]:)?(\d+)", re.IGNORECASE)
RE_SSL_CERT = re.compile(r"ssl_certificate\s+", re.IGNORECASE)
RE_PROXY_PASS = re.compile(r"proxy_pass\s+", re.IGNORECASE)


def parse_site_config(file_path: Path) -> tuple[list[str], list[int], bool, bool]:
    """Parse key directives from an Nginx configuration file.
    
    Returns tuple of (domains, ports, has_ssl, is_proxy).
    """
    if not file_path.is_file():
        return [], [], False, False

    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return [], [], False, False

    domains: set[str] = set()
    for match in RE_SERVER_NAME.finditer(content):
        names = match.group(1).split()
        for name in names:
            clean = name.strip()
            if clean and clean != "_":
                domains.add(clean)

    ports: set[int] = set()
    for match in RE_LISTEN_PORT.finditer(content):
        try:
            ports.add(int(match.group(1)))
        except ValueError:
            pass

    has_ssl = bool(RE_SSL_CERT.search(content))
    is_proxy = bool(RE_PROXY_PASS.search(content))

    return sorted(domains), sorted(ports), has_ssl, is_proxy


def get_site_info(site_name: str, paths: NginxPaths) -> SiteInfo | None:
    """Inspect and retrieve status details for a specific site by name."""
    clean_name = site_name.removesuffix(".conf")
    conf_name = f"{clean_name}.conf"

    avail_path: Path | None = None
    enabled_path: Path | None = None

    if paths.uses_sites_structure:
        if paths.sites_available:
            p = paths.sites_available / conf_name
            p_noext = paths.sites_available / clean_name
            avail_path = p if p.exists() else (p_noext if p_noext.exists() else None)

        if paths.sites_enabled:
            p = paths.sites_enabled / conf_name
            p_noext = paths.sites_enabled / clean_name
            enabled_path = p if (p.exists() or p.is_symlink()) else (p_noext if (p_noext.exists() or p_noext.is_symlink()) else None)
    else:
        if paths.conf_d:
            p = paths.conf_d / conf_name
            if p.exists():
                avail_path = p
                enabled_path = p

    if not avail_path and not enabled_path:
        return None

    target_parse_path = avail_path or enabled_path
    domains, ports, has_ssl, is_proxy = parse_site_config(target_parse_path) if target_parse_path else ([], [], False, False)
    is_enabled = enabled_path is not None and (enabled_path.exists() or enabled_path.is_symlink())

    return SiteInfo(
        name=clean_name,
        available_path=avail_path,
        enabled_path=enabled_path,
        is_enabled=is_enabled,
        domains=domains,
        ports=ports,
        has_ssl=has_ssl,
        is_proxy=is_proxy,
    )


def list_all_sites(paths: NginxPaths) -> list[SiteInfo]:
    """Discover and return status details for all sites in Nginx directories."""
    sites_map: dict[str, SiteInfo] = {}

    # Discover from sites-available or conf.d
    search_dirs = []
    if paths.uses_sites_structure and paths.sites_available:
        search_dirs.append(paths.sites_available)
    elif paths.conf_d:
        search_dirs.append(paths.conf_d)

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        for file_path in search_dir.glob("*"):
            if file_path.is_file() and not file_path.name.startswith("."):
                site_name = file_path.name.removesuffix(".conf")
                info = get_site_info(site_name, paths)
                if info:
                    sites_map[site_name] = info

    # Discover enabled sites that might missing from available (orphaned symlinks)
    if paths.uses_sites_structure and paths.sites_enabled and paths.sites_enabled.exists():
        for file_path in paths.sites_enabled.glob("*"):
            site_name = file_path.name.removesuffix(".conf")
            if site_name not in sites_map:
                info = get_site_info(site_name, paths)
                if info:
                    sites_map[site_name] = info

    return sorted(sites_map.values(), key=lambda s: s.name)