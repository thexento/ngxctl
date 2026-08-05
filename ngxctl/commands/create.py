"""Interactive and fast CLI command handlers for generating Nginx site configurations."""

import socket
from pathlib import Path
import click

from ngxctl.config import AppConfig
from ngxctl.core.backup import create_backup
from ngxctl.core.generator import ConfigGenerator, SiteContext
from ngxctl.core.system import enable_site, reload_nginx, test_config
from ngxctl.utils import console
from ngxctl.utils.fs import atomic_write, can_write, check_root_or_elevate


def _get_default_ip() -> str:
    """Best-effort discovery of local or public IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "_"


@click.group(name="create", invoke_without_command=True)
@click.pass_context
def create_group(ctx: click.Context) -> None:
    """Generate new Nginx site configurations (Interactive by default)."""
    if ctx.invoked_subcommand is None:
        _run_interactive_wizard(ctx)


def _run_interactive_wizard(ctx: click.Context) -> None:
    """Guided wizard for fast site creation with smart defaults."""
    app_config: AppConfig = ctx.obj["config"]
    paths = app_config.nginx_paths

    # STEP 0: Pre-check permissions and elevate before asking any questions
    target_dir = (
        paths.sites_available
        if (paths.uses_sites_structure and paths.sites_available)
        else (paths.conf_d or paths.nginx_dir)
    )

    if not can_write(target_dir):
        if not check_root_or_elevate(f"write operations in '{target_dir}'"):
            return

    console.info("Welcome to the ngxctl site configuration wizard!")

    # 1. Project / Site Name prompt
    default_site_name = Path.cwd().name or "mysite"
    site_name_input = click.prompt(
        "Project / Site name",
        default=default_site_name,
        show_default=True,
    )
    site_name = site_name_input.strip().replace(" ", "-")

    # 2. Domain prompt
    default_ip = _get_default_ip()
    domain_input = click.prompt(
        "Domain name (or press Enter for IP/catch-all)",
        default=default_ip,
        show_default=True,
    )
    domains = [d.strip() for d in domain_input.split() if d.strip()]

    # 3. Site type prompt
    click.echo("\nSelect Site Type:")
    click.echo("  [1] Reverse Proxy (Node.js, Python, Flask, FastAPI, Docker, Go)")
    click.echo("  [2] Static Website / SPA (React, Vue, HTML/JS)")
    click.echo("  [3] PHP Application (WordPress, Laravel)")

    site_type = click.prompt("Choice", type=click.Choice(["1", "2", "3"]), default="1")

    # Collect parameters based on site type
    root_dir: str | None = None
    entrypoint = "index.html"
    proxy_pass_url: str | None = None
    is_spa = False
    enable_websocket = False

    if site_type == "1":  # Reverse Proxy
        port = click.prompt("Backend port or URL", default="3000")
        if not port.startswith("http://") and not port.startswith("https://"):
            proxy_pass_url = f"http://127.0.0.1:{port}"
        else:
            proxy_pass_url = port
        enable_websocket = click.confirm("Enable WebSocket support?", default=True)

    elif site_type == "2":  # Static / SPA
        cwd = str(Path.cwd().resolve())
        root_dir = click.prompt("Root directory path", default=cwd)
        entrypoint = click.prompt("Entrypoint HTML file", default="index.html")
        is_spa = click.confirm("Is this a Single Page App (React/Vue router)?", default=False)

    elif site_type == "3":  # PHP
        cwd = str(Path.cwd().resolve())
        root_dir = click.prompt("Root directory path", default=cwd)

    # 4. Quick Setup vs Detailed Setup
    quick_mode = click.confirm("\nPerform quick automatic setup (auto-enable, test & reload)?", default=True)

    ssl_enabled = False
    ssl_cert_path: str | None = None
    ssl_key_path: str | None = None
    force_https = False

    if not quick_mode:
        ssl_enabled = click.confirm("Configure SSL manually?", default=False)
        if ssl_enabled:
            ssl_cert_path = click.prompt("Path to SSL Certificate (.crt/.pem)")
            ssl_key_path = click.prompt("Path to SSL Private Key (.key)")
            force_https = click.confirm("Redirect HTTP to HTTPS?", default=True)

    template_map = {"1": "reverse_proxy.j2", "2": "static.j2", "3": "php.j2"}

    context = SiteContext(
        domains=domains,
        listen_port=80,
        ssl_enabled=ssl_enabled,
        ssl_cert_path=ssl_cert_path,
        ssl_key_path=ssl_key_path,
        force_https=force_https,
        root_dir=root_dir,
        entrypoint=entrypoint,
        is_spa=is_spa,
        proxy_pass_url=proxy_pass_url,
        enable_websocket=enable_websocket,
    )

    _write_and_process_config(
        app_config=app_config,
        template_name=template_map[site_type],
        context=context,
        site_name=site_name,
        auto_enable=quick_mode,
        run_test=quick_mode,
        auto_reload=quick_mode,
    )


@create_group.command(name="reverse-proxy")
@click.option("--site-name", "-n", default=None, help="Project / Site configuration name.")
@click.option("--domain", "-d", multiple=True, help="Domain name(s). Defaults to server IP.")
@click.option("--port", "-p", default="3000", help="Backend port or proxy URL (default: 3000).")
@click.option("--websocket/--no-websocket", default=True, help="Enable WebSocket proxy headers.")
@click.option("--enable/--no-enable", default=True, help="Auto-enable site symlink.")
@click.option("--reload/--no-reload", default=True, help="Auto-reload Nginx if test passes.")
@click.pass_context
def create_reverse_proxy(
    ctx: click.Context,
    site_name: str | None,
    domain: tuple[str, ...],
    port: str,
    websocket: bool,
    enable: bool,
    reload: bool,
) -> None:
    """Quickly create a reverse proxy site."""
    domains = list(domain) if domain else [_get_default_ip()]
    name = site_name or domains[0]
    proxy_url = port if port.startswith("http") else f"http://127.0.0.1:{port}"

    context = SiteContext(
        domains=domains,
        listen_port=80,
        proxy_pass_url=proxy_url,
        enable_websocket=websocket,
    )

    app_config: AppConfig = ctx.obj["config"]
    _write_and_process_config(
        app_config=app_config,
        template_name="reverse_proxy.j2",
        context=context,
        site_name=name,
        auto_enable=enable,
        run_test=True,
        auto_reload=reload,
    )


@create_group.command(name="static")
@click.option("--site-name", "-n", default=None, help="Project / Site configuration name.")
@click.option("--domain", "-d", multiple=True, help="Domain name(s). Defaults to server IP.")
@click.option("--root", "-r", default=None, help="Root folder (default: current working directory).")
@click.option("--entrypoint", "-e", default="index.html", help="Main HTML file (default: index.html).")
@click.option("--spa/--no-spa", default=False, help="Enable SPA client routing (React/Vue).")
@click.option("--enable/--no-enable", default=True, help="Auto-enable site symlink.")
@click.option("--reload/--no-reload", default=True, help="Auto-reload Nginx if test passes.")
@click.pass_context
def create_static(
    ctx: click.Context,
    site_name: str | None,
    domain: tuple[str, ...],
    root: str | None,
    entrypoint: str,
    spa: bool,
    enable: bool,
    reload: bool,
) -> None:
    """Quickly create a static website or SPA site."""
    domains = list(domain) if domain else [_get_default_ip()]
    name = site_name or Path.cwd().name
    root_path = root or str(Path.cwd().resolve())

    context = SiteContext(
        domains=domains,
        listen_port=80,
        root_dir=root_path,
        entrypoint=entrypoint,
        is_spa=spa,
    )

    app_config: AppConfig = ctx.obj["config"]
    _write_and_process_config(
        app_config=app_config,
        template_name="static.j2",
        context=context,
        site_name=name,
        auto_enable=enable,
        run_test=True,
        auto_reload=reload,
    )


def _write_and_process_config(
    app_config: AppConfig,
    template_name: str,
    context: SiteContext,
    site_name: str,
    auto_enable: bool,
    run_test: bool,
    auto_reload: bool = False,
) -> None:
    """Render, write, enable, test, and reload configuration."""
    paths = app_config.nginx_paths
    generator = ConfigGenerator(app_config)

    try:
        content = generator.render(template_name, context)
    except ValueError as err:
        console.error(f"Validation error: {err}")
        return

    # Choose target directory
    if paths.uses_sites_structure and paths.sites_available:
        target_dir = paths.sites_available
    elif paths.conf_d:
        target_dir = paths.conf_d
    else:
        target_dir = paths.nginx_dir

    # Pre-check permission & elevate before writing
    if not can_write(target_dir):
        if not check_root_or_elevate(f"write operations in '{target_dir}'"):
            return

    config_path = target_dir / f"{site_name}.conf"

    # Backup if file exists
    if config_path.exists():
        backup_file = create_backup(site_name, config_path, app_config.backup_dir)
        console.info(f"Existing configuration backed up to '{backup_file.name}'.")

    atomic_write(config_path, content)
    console.success(f"Configuration generated: '{config_path}'")

    if auto_enable and paths.uses_sites_structure:
        try:
            enabled_link = enable_site(site_name, paths)
            console.success(f"Site enabled: '{enabled_link.name}'")
        except Exception as err:
            console.error(f"Failed to enable site: {err}")

    if run_test:
        test_res = test_config()
        if test_res.success:
            console.success("Nginx configuration test passed (nginx -t).")
            if auto_reload:
                reload_res = reload_nginx()
                if reload_res.success:
                    console.success("Nginx reloaded successfully!")
                else:
                    console.warning(f"Failed to reload Nginx: {reload_res.stderr}")
        else:
            console.error(f"Nginx syntax error:\n{test_res.stderr}")