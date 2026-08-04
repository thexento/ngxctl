
# ngxctl

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**ngxctl** is a modern, fast, human-friendly command-line utility for generating, managing, validating, and applying Nginx configurations.

It automates repetitive Nginx web server management tasks—from generating reverse proxy blocks for Node.js/Python apps to managing active sites and creating automatic snapshot backups—while producing clean, human-readable configuration files.

---

## Key Features

- **Interactive Setup Wizard**: Run `ngxctl create` to launch a guided, 3-question setup with smart defaults (auto-detects server IP, current working directory, and backend ports).
- **Reverse Proxy Support**: Built-in support for Node.js, Python (Flask, Django, FastAPI), Docker, Go, and WebSocket upgrade headers.
- **Static Sites & SPAs**: Native support for static file hosting and Single Page Application (React, Vue, Svelte) client-side routing.
- **PHP Applications**: Configured for FastCGI PHP-FPM servers (Laravel, WordPress).
- **Site Management**: Simple subcommands to list, inspect, enable, or disable sites without manually managing `/etc/nginx/sites-enabled/` symlinks.
- **Service Control**: Integrated syntax testing (`nginx -t`), non-disruptive reloading, and restarting.
- **Snapshot Backups**: Atomic, timestamped backup snapshots created automatically before configuration overwrites, with full rollback/restore support.

---

## Installation

### Prerequisites

- Python 3.12 or higher
- Nginx web server installed on host

### Install via pipx (Recommended)

```bash
pipx install git+https://github.com/thexento/ngxctl.git

Install in Editable / Development Mode

git clone https://github.com/thexento/ngxctl.git
cd ngxctl
pip install -e .

Quickstart & Usage

1. Interactive Site Creation (Fastest)

Simply run ngxctl create without arguments to launch the interactive wizard:

ngxctl create

Wizard Flow:

1.  Enter domain name (defaults to server IP or _).
2.  Select site type (Reverse Proxy, Static/SPA, PHP).
3.  Confirm quick setup (automatically generates config, links symlink, runs
    nginx -t, and reloads Nginx).

2. Flag-Driven Commands

Reverse Proxy

# Create reverse proxy for app running on port 3000
ngxctl create reverse-proxy -d app.example.com -p 3000

# Specify custom backend URL with WebSockets
ngxctl create reverse-proxy -d app.example.com -p http://127.0.0.1:8080 --websocket

Static Website / SPA

# Serve static site from current directory
ngxctl create static -d example.com

# Serve React/Vue SPA with client-side routing fallback
ngxctl create static -d spa.example.com -r /var/www/my-app/dist --spa

PHP Application

ngxctl create php -d php.example.com -r /var/www/wordpress

3. Managing Sites

# List all configured sites and active status
ngxctl list

# Inspect detailed status and directives for a site
ngxctl inspect mysite

# Enable a site (creates symlink in sites-enabled & reloads)
ngxctl enable mysite

# Disable a site (removes symlink & reloads)
ngxctl disable mysite

4. Service Operations & Syntax Testing

# Test Nginx syntax (nginx -t)
ngxctl test

# Reload Nginx safely (tests syntax first)
ngxctl reload

# Restart Nginx service
ngxctl restart

5. Snapshot Backups & Restoration

# Create an on-demand snapshot backup
ngxctl backup create mysite

# List all stored snapshots
ngxctl backup list

# Interactively select and restore a backup snapshot
ngxctl backup restore mysite

Environment Variable Overrides

Custom Nginx directory paths can be overridden using environment variables:

| Variable                 | Description                                  |
| :----------------------- | :------------------------------------------- |
| `NGXCTL_NGINX_DIR`       | Base Nginx directory (default: `/etc/nginx`) |
| `NGXCTL_SITES_AVAILABLE` | Path to `sites-available`                    |
| `NGXCTL_SITES_ENABLED`   | Path to `sites-enabled`                      |
| `NGXCTL_CONF_D`          | Path to `conf.d`                             |
| `NGXCTL_BACKUP_DIR`      | Custom backup snapshot directory             |

License

Distributed under the MIT License. See LICENSE for details.

Author: Xento (@thexento)


---

File completed. Please request `.gitignore` or `LICENSE`.
