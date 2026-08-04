"""Configuration backup, restoration, and snapshot lifecycle management."""

import shutil
from datetime import datetime
from pathlib import Path

from ngxctl.utils.fs import atomic_write, ensure_directory


def generate_backup_filename(site_name: str) -> str:
    """Generate a timestamped backup filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_site_name = site_name.removesuffix(".conf")
    return f"{clean_site_name}_{timestamp}.conf"


def create_backup(site_name: str, source_path: Path, backup_dir: Path) -> Path:
    """Create a timestamped backup copy of an existing Nginx configuration file.
    
    Raises FileNotFoundError if source_path does not exist.
    """
    if not source_path.exists():
        raise FileNotFoundError(f"Configuration file to backup not found at '{source_path}'")

    ensure_directory(backup_dir)
    backup_filename = generate_backup_filename(site_name)
    backup_path = backup_dir / backup_filename

    shutil.copy2(source_path, backup_path)
    return backup_path


def list_backups(backup_dir: Path, site_name: str | None = None) -> list[Path]:
    """List all available configuration backups sorted by creation time (newest first).
    
    If site_name is provided, filters backups for that specific site.
    """
    if not backup_dir.exists():
        return []

    clean_name = site_name.removesuffix(".conf") if site_name else None
    backups = []

    for file_path in backup_dir.glob("*.conf"):
        if clean_name:
            if file_path.name.startswith(f"{clean_name}_"):
                backups.append(file_path)
        else:
            backups.append(file_path)

    # Sort by modification time descending (newest first)
    backups.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return backups


def restore_backup(backup_path: Path, target_path: Path) -> None:
    """Restore a backup configuration file to its active site location atomically.
    
    Raises FileNotFoundError if the backup_path does not exist.
    """
    if not backup_path.exists():
        raise FileNotFoundError(f"Backup file '{backup_path}' does not exist.")

    content = backup_path.read_text(encoding="utf-8")
    atomic_write(target_path, content)


def prune_backups(backup_dir: Path, site_name: str, keep_count: int = 5) -> int:
    """Prune older backups for a site, retaining only the most recent keep_count entries.
    
    Returns the count of removed backup files.
    """
    backups = list_backups(backup_dir, site_name)
    if len(backups) <= keep_count:
        return 0

    to_delete = backups[keep_count:]
    removed_count = 0
    for file_path in to_delete:
        file_path.unlink(missing_ok=True)
        removed_count += 1

    return removed_count