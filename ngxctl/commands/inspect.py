"""CLI subcommands for inspecting and listing Nginx site configurations."""

import click

from ngxctl.config import AppConfig
from ngxctl.core.inspector import get_site_info, list_all_sites
from ngxctl.utils import console


@click.command(name="list")
@click.pass_context
def list_cmd(ctx: click.Context) -> None:
    """List all detected Nginx site configurations and their active status."""
    app_config: AppConfig = ctx.obj["config"]
    paths = app_config.nginx_paths

    sites = list_all_sites(paths)
    if not sites:
        console.info("No Nginx site configurations found.")
        return

    click.echo(f"\nDiscovered {len(sites)} site(s):\n")
    header = f"{'SITE NAME':<20} {'STATUS':<12} {'TYPE':<15} {'PORTS':<10} {'DOMAINS'}"
    click.echo(click.style(header, bold=True, underline=True))

    for site in sites:
        status_str = (
            click.style("ENABLED ", fg="green", bold=True)
            if site.is_enabled
            else click.style("DISABLED", fg="yellow")
        )
        site_type = "Proxy" if site.is_proxy else "Static/App"
        ports_str = ",".join(str(p) for p in site.ports) or "80"
        domains_str = ", ".join(site.domains) if site.domains else "-"

        click.echo(f"{site.name:<20} {status_str:<12} {site_type:<15} {ports_str:<10} {domains_str}")

    click.echo("")


@click.command(name="inspect")
@click.argument("site_name", required=False)
@click.option("--show-code/--no-show-code", "-c", default=False, help="Print config file contents.")
@click.pass_context
def inspect_cmd(ctx: click.Context, site_name: str | None, show_code: bool) -> None:
    """Inspect detailed status and configuration for a specific site."""
    app_config: AppConfig = ctx.obj["config"]
    paths = app_config.nginx_paths

    if not site_name:
        all_sites = list_all_sites(paths)
        if not all_sites:
            console.info("No Nginx sites found to inspect.")
            return

        click.echo("Select a site to inspect:")
        for idx, site in enumerate(all_sites, start=1):
            click.echo(f"  [{idx}] {site.name}")

        choice = click.prompt("Choice", type=click.IntRange(1, len(all_sites)))
        site_name = all_sites[choice - 1].name

    site_info = get_site_info(site_name, paths)
    if not site_info:
        console.error(f"Site '{site_name}' was not found in Nginx configuration directories.")
        return

    click.echo("\n" + click.style(f"=== Site Details: {site_info.name} ===", bold=True, fg="cyan"))
    
    status_label = click.style("ENABLED", fg="green", bold=True) if site_info.is_enabled else click.style("DISABLED", fg="yellow")
    click.echo(f"Status:             {status_label}")
    click.echo(f"Domains:            {', '.join(site_info.domains) or 'None'}")
    click.echo(f"Ports:              {', '.join(str(p) for p in site_info.ports) or '80'}")
    click.echo(f"SSL Configured:     {'Yes' if site_info.has_ssl else 'No'}")
    click.echo(f"Reverse Proxy:      {'Yes' if site_info.is_proxy else 'No'}")
    
    if site_info.available_path:
        click.echo(f"Available Path:     {site_info.available_path}")
    if site_info.enabled_path:
        click.echo(f"Enabled Symlink:    {site_info.enabled_path}")

    # Output file content if requested
    target_file = site_info.available_path or site_info.enabled_path
    if show_code and target_file and target_file.is_file():
        click.echo("\n" + click.style("--- Configuration Preview ---", bold=True))
        try:
            content = target_file.read_text(encoding="utf-8")
            click.echo(content)
        except OSError as err:
            console.error(f"Failed to read file contents: {err}")
    click.echo("")