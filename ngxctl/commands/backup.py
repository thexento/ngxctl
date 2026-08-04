"""CLI subcommands for managing site configuration backups and snapshots."""

import click

from ngxctl.config import AppConfig
from ngxctl.core.backup import create_backup, list_backups, restore_backup
from ngxctl.core.inspector import get_site_info, list_all_sites
from ngxctl.core.system import reload_nginx, test_config
from ngxctl.utils import console


@click.group(name="backup")
def backup_group() -> None:
    """Create, list, and restore site configuration backups."""


@backup_group.command(name="create")
@click.argument("site_name", required=False)
@click.pass_context
def create_backup_cmd(ctx: click.Context, site_name: str | None) -> None:
    """Create a manual timestamped backup snapshot of a site configuration."""
    app_config: AppConfig = ctx.obj["config"]
    paths = app_config.nginx_paths

    if not site_name:
        all_sites = list_all_sites(paths)
        if not all_sites:
            console.info("No sites available to backup.")
            return

        click.echo("Select a site to backup:")
        for idx, site in enumerate(all_sites, start=1):
            click.echo(f"  [{idx}] {site.name}")

        choice = click.prompt("Choice", type=click.IntRange(1, len(all_sites)))
        site_name = all_sites[choice - 1].name

    site_info = get_site_info(site_name, paths)
    if not site_info or not (site_info.available_path or site_info.enabled_path):
        console.error(f"Site '{site_name}' does not exist.")
        return

    source_file = site_info.available_path or site_info.enabled_path
    if not source_file:
        console.error(f"Could not find configuration file for site '{site_name}'.")
        return

    try:
        backup_file = create_backup(site_name, source_file, app_config.backup_dir)
        console.success(f"Backup snapshot created: '{backup_file.name}' in {app_config.backup_dir}")
    except Exception as err:
        console.error(f"Failed to create backup: {err}")


@backup_group.command(name="list")
@click.argument("site_name", required=False)
@click.pass_context
def list_backups_cmd(ctx: click.Context, site_name: str | None) -> None:
    """List stored configuration backups."""
    app_config: AppConfig = ctx.obj["config"]
    backups = list_backups(app_config.backup_dir, site_name)

    if not backups:
        console.info(f"No backups found in {app_config.backup_dir}")
        return

    click.echo(f"\nStored Backups ({len(backups)}):\n")
    header = f"{'BACKUP FILE':<40} {'SIZE':<10}"
    click.echo(click.style(header, bold=True, underline=True))

    for b in backups:
        size_kb = f"{b.stat().st_size / 1024:.1f} KB"
        click.echo(f"{b.name:<40} {size_kb:<10}")
    click.echo("")


@backup_group.command(name="restore")
@click.argument("site_name", required=False)
@click.option("--reload/--no-reload", default=True, help="Auto-reload Nginx after restoration.")
@click.pass_context
def restore_backup_cmd(ctx: click.Context, site_name: str | None, reload: bool) -> None:
    """Restore a previous configuration snapshot for a site."""
    app_config: AppConfig = ctx.obj["config"]
    paths = app_config.nginx_paths

    backups = list_backups(app_config.backup_dir, site_name)
    if not backups:
        console.info("No backups found to restore.")
        return

    click.echo("\nSelect a backup snapshot to restore:")
    for idx, b_file in enumerate(backups, start=1):
        click.echo(f"  [{idx}] {b_file.name}")

    choice = click.prompt("Choice", type=click.IntRange(1, len(backups)))
    selected_backup = backups[choice - 1]

    # Extract site name from filename prefix
    target_site_name = site_name or selected_backup.name.split("_")[0]
    site_info = get_site_info(target_site_name, paths)

    if site_info and site_info.available_path:
        target_path = site_info.available_path
    elif paths.uses_sites_structure and paths.sites_available:
        target_path = paths.sites_available / f"{target_site_name}.conf"
    elif paths.conf_d:
        target_path = paths.conf_d / f"{target_site_name}.conf"
    else:
        target_path = paths.nginx_dir / f"{target_site_name}.conf"

    try:
        restore_backup(selected_backup, target_path)
        console.success(f"Restored backup '{selected_backup.name}' to '{target_path}'.")
    except Exception as err:
        console.error(f"Failed to restore backup: {err}")
        return

    if reload:
        test_res = test_config()
        if test_res.success:
            reload_res = reload_nginx()
            if reload_res.success:
                console.success("Nginx validated and reloaded successfully.")
            else:
                console.warning(f"Failed to reload Nginx: {reload_res.stderr}")
        else:
            console.error(f"Restored configuration failed syntax test:\n{test_res.stderr}")