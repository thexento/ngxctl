"""Template rendering engine and context builder for Nginx configuration generation."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, TemplateNotFound

from ngxctl.config import AppConfig


@dataclass(slots=True)
class SiteContext:
    """Configuration context parameters passed to Nginx Jinja2 templates."""

    domains: list[str]
    listen_port: int = 80
    ssl_enabled: bool = False
    ssl_cert_path: str | None = None
    ssl_key_path: str | None = None
    force_https: bool = False

    # Static Site / SPA fields
    root_dir: str | None = None
    entrypoint: str = "index.html"
    index_files: list[str] = field(default_factory=lambda: ["index.html", "index.htm"])
    is_spa: bool = False  # Enable try_files $uri $uri/ /entrypoint

    # Reverse Proxy / App Backend fields
    proxy_pass_url: str | None = None
    enable_websocket: bool = False
    client_max_body_size: str = "10M"

    def validate(self) -> None:
        """Validate context consistency before rendering."""
        if not self.domains:
            raise ValueError("At least one domain name must be provided.")

        if self.ssl_enabled and not (self.ssl_cert_path and self.ssl_key_path):
            raise ValueError(
                "When SSL is enabled, both 'ssl_cert_path' and 'ssl_key_path' must be provided."
            )

        if not self.root_dir and not self.proxy_pass_url:
            raise ValueError(
                "Site context must specify either a 'root_dir' (static) or 'proxy_pass_url' (proxy)."
            )

    def to_dict(self) -> dict[str, Any]:
        """Convert context dataclass to dictionary for Jinja2 rendering."""
        self.validate()
        primary_domain = self.domains[0]
        server_name_str = " ".join(self.domains)

        # Build index files list with primary entrypoint first
        ordered_indices = [self.entrypoint]
        for f in self.index_files:
            if f not in ordered_indices:
                ordered_indices.append(f)

        return {
            "domains": self.domains,
            "primary_domain": primary_domain,
            "server_name": server_name_str,
            "listen_port": self.listen_port,
            "ssl_enabled": self.ssl_enabled,
            "ssl_cert_path": self.ssl_cert_path,
            "ssl_key_path": self.ssl_key_path,
            "force_https": self.force_https,
            "root_dir": self.root_dir,
            "entrypoint": self.entrypoint,
            "index_files": " ".join(ordered_indices),
            "is_spa": self.is_spa,
            "proxy_pass_url": self.proxy_pass_url,
            "enable_websocket": self.enable_websocket,
            "client_max_body_size": self.client_max_body_size,
        }


class ConfigGenerator:
    """Nginx configuration generator using Jinja2 templates."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self._env = self._build_environment()

    def _build_environment(self) -> Environment:
        """Construct Jinja2 environment with custom user directory fallback to built-ins."""
        builtin_templates_dir = Path(__file__).parent.parent / "templates"

        loaders = []
        if self.config.user_templates_dir.exists():
            loaders.append(FileSystemLoader(self.config.user_templates_dir))
        loaders.append(FileSystemLoader(builtin_templates_dir))

        return Environment(
            loader=ChoiceLoader(loaders),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
            autoescape=False,  # Plain text Nginx config, no HTML escaping
        )

    def render(self, template_name: str, context: SiteContext) -> str:
        """Render an Nginx configuration template with the given site context.

        Template name should include the extension (e.g. 'reverse_proxy.j2', 'static.j2').
        """
        if not template_name.endswith(".j2"):
            template_name = f"{template_name}.j2"

        try:
            template = self._env.get_template(template_name)
        except TemplateNotFound as err:
            raise FileNotFoundError(
                f"Template '{template_name}' not found in user or built-in template directories."
            ) from err

        return template.render(**context.to_dict())