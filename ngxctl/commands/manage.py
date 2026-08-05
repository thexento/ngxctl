"""CLI subcommands for managing site states and Nginx service lifecycle."""

import click

from ngxctl.config import AppConfig
from ngxctl.core.inspector import list_all_sites
from ngxctl.core.system import (
    disable_site,
    enable_site,
    reload_nginx,
    restart_nginx,
    test_config,
)
from ngxctl.utils import console
from ngxctl.utils.fs import can_write, check_root_or_elevate, is_root


@click.command(name="enable")
@click.argument("site_name", required=False)
@click.option("--reload/--no-reload", default=True, help="Auto-reload Nginx after enabling site.")
@click.pass_context
def enable_cmd(ctx: click.Context, site_name: str | None, reload: bool) -> None:
    """Enable a site configuration by linking sites-available to sites-enabled."""
    app_config: AppConfig = ctx.obj["config"]
    paths = app_config.nginx_paths

    if not paths.uses_sites_structure:
        console.warning("This system uses conf.d structure; sites are active directly without symlinks.")
        return

    # Check root permission before symlinking
    target_dir = paths.sites_enabled or paths.nginx_dir
    if not can_write(target_dir):
        if not check_root_or_elevate("enabling site configurations"):
            return

    # Interactive selection if site_name is not provided
    if not site_name:
        all_sites = list_all_sites(paths)
        disabled_sites = [s for s in all_sites if not s.is_enabled and s.available_path]

        if not disabled_sites:
            console.info("No disabled sites found to enable.")
            return

        click.echo("Select a site to enable:")
        for idx, site in enumerate(disabled_sites, start=1):
            click.echo(f"  [{idx}] {site.name} ({', '.join(site.domains) or 'no domain'})")

        choice = click.prompt("Choice", type=click.IntRange(1, len(disabled_sites)))
        site_name = disabled_sites[choice - 1].name

    try:
        enabled_link = enable_site(site_name, paths)
        console.success(f"Site '{site_name}' enabled ({enabled_link}).")
    except FileNotFoundError:
        console.error(f"Site '{site_name}' not found in sites-available.")
        return
    except Exception as err:
        console.error(f"Failed to enable site '{site_name}': {err}")
        return

    if reload:
        _test_and_reload()


@click.command(name="disable")
@click.argument("site_name", required=False)
@click.option("--reload/--no-reload", default=True, help="Auto-reload Nginx after disabling site.")
@click.pass_context
def disable_cmd(ctx: click.Context, site_name: str | None, reload: bool) -> None:
    """Disable a site configuration by removing its symlink from sites-enabled."""
    app_config: AppConfig = ctx.obj["config"]
    paths = app_config.nginx_paths

    if not paths.uses_sites_structure:
        console.warning("This system uses conf.d structure; disable by removing/moving the .conf file.")
        return

    # Check root permission before removing symlink
    target_dir = paths.sites_enabled or paths.nginx_dir
    if not can_write(target_dir):
        if not check_root_or_elevate("disabling site configurations"):
            return

    # Interactive selection if site_name is not provided
    if not site_name:
        all_sites = list_all_sites(paths)
        enabled_sites = [s for s in all_sites if s.is_enabled]

        if not enabled_sites:
            console.info("No active/enabled sites found to disable.")
            return

        click.echo("Select a site to disable:")
        for idx, site in enumerate(enabled_sites, start=1):
            click.echo(f"  [{idx}] {site.name} ({', '.join(site.domains) or 'no domain'})")

        choice = click.prompt("Choice", type=click.IntRange(1, len(enabled_sites)))
        site_name = enabled_sites[choice - 1].name

    try:
        was_disabled = disable_site(site_name, paths)
        if was_disabled:
            console.success(f"Site '{site_name}' disabled.")
        else:
            console.warning(f"Site '{site_name}' was not currently enabled.")
            return
    except Exception as err:
        console.error(f"Failed to disable site '{site_name}': {err}")
        return

    if reload:
        _test_and_reload()


@click.command(name="test")
def test_cmd() -> None:
    """Validate Nginx configuration syntax (nginx -t)."""
    res = test_config()
    if res.success:
        console.success("Nginx configuration syntax is OK.")
        if res.stderr:
            click.echo(res.stderr)
    else:
        console.error("Nginx configuration test failed!")
        if res.stderr:
            click.echo(res.stderr, err=True)


@click.command(name="reload")
def reload_cmd() -> None:
    """Reload Nginx service without dropping connections."""
    if not is_root():
        if not check_root_or_elevate("reloading Nginx service"):
            return
    _test_and_reload()


@click.command(name="restart")
def restart_cmd() -> None:
    """Restart Nginx service."""
    if not is_root():
        if not check_root_or_elevate("restarting Nginx service"):
            return

    console.info("Validating Nginx syntax before restart...")
    test_res = test_config()
    if not test_res.success:
        console.error(f"Cannot restart: Syntax test failed!\n{test_res.stderr}")
        return

    restart_res = restart_nginx()
    if restart_res.success:
        console.success("Nginx service restarted successfully.")
    else:
        console.error(f"Failed to restart Nginx: {restart_res.stderr}")


def _test_and_reload() -> None:
    """Validate syntax and reload Nginx service."""
    test_res = test_config()
    if not test_res.success:
        console.error(f"Cannot reload: Nginx syntax test failed!\n{test_res.stderr}")
        return

    reload_res = reload_nginx()
    if reload_res.success:
        console.success("Nginx reloaded successfully.")
    else:
        console.error(f"Failed to reload Nginx: {reload_res.stderr}")