
<div align="center">

<img src="public/ngxctl-banner.png"
     alt="ngxctl Banner"
     width="150">

<br>


# ngxctl

**A modern command-line utility for generating, managing, validating, and deploying Nginx configurations.**

<p>

<a href="https://www.python.org/downloads/">
<img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white">
</a>

<a href="https://pypi.org/project/ngxctl-cli/">
<img src="https://img.shields.io/pypi/v/ngxctl-cli?style=for-the-badge&color=009639">
</a>

<a href="https://nginx.org/">
<img src="https://img.shields.io/badge/Nginx-Supported-009639?style=for-the-badge&logo=nginx&logoColor=white">
</a>

<a href="LICENSE">
<img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge">
</a>

<img src="https://img.shields.io/badge/Linux-Supported-FCC624?style=for-the-badge&logo=linux&logoColor=black">

</p>

*A cleaner way to work with Nginx.*

</div>

---

# Overview

`ngxctl` is an open-source command-line utility that simplifies creating, managing, validating, and deploying Nginx configurations.

Whether you're deploying a personal website, hosting a production API, or managing multiple virtual hosts on a VPS, `ngxctl` removes repetitive work while generating clean, readable, and fully editable Nginx configuration files.

Instead of manually writing server blocks, enabling sites, validating syntax, and reloading Nginx, `ngxctl` automates the entire workflow through a simple command-line interface.

> **It doesn't replace Nginx—it makes working with Nginx faster.**

---

# Why ngxctl?

Working with Nginx usually means repeating the same workflow:

- Create a configuration
- Copy an existing server block
- Change the domain
- Change the backend port
- Enable the site
- Test the configuration
- Reload Nginx

Do that often enough and it becomes repetitive.

`ngxctl` automates those repetitive steps while still producing standard Nginx configuration files that remain completely editable.

---

# Features

## Configuration Generation

- Interactive setup wizard
- Smart defaults
- Automatic `sudo` privilege elevation
- Reverse proxy generation
- Static website hosting
- SPA support (React, Vue, Svelte)
- Custom entrypoint support
- PHP-FPM templates
- Docker reverse proxy templates
- WebSocket support
- SSL-ready templates
- HTTP → HTTPS redirects

## Supported Technologies

**Reverse Proxies**
- Node.js
- Express
- NestJS
- FastAPI
- Flask
- Django
- Go
- PHP-FPM

**Frontend Applications**
- React
- Vue
- Svelte
- Static Websites

**Deployment Targets**
- Docker Containers

## Site Management

- Create sites
- Enable sites
- Disable sites
- List configured sites
- Inspect configurations
- Automatic symlink management

---

## Service Management

- Validate configurations
- Reload Nginx
- Restart Nginx
- Safe validation before reload

---

## Backup & Recovery

- Automatic snapshots
- Timestamped backups
- Restore previous configurations
- Backup listing
- Rollback support

---

# Installation

## Requirements

- Python **3.12+**
- Nginx
- Linux

---

## Install from PyPI

```bash
pip install ngxctl-cli
```

---

## Install with pipx

```bash
pipx install ngxctl-cli
```

---

## Install from Source

Clone the repository:

```bash
git clone https://github.com/thexento/ngxctl.git
cd ngxctl
```

Install in editable mode:

```bash
pip install -e .
```

---

# Quick Start

Launch the interactive setup wizard:

```bash
ngxctl create
```

The wizard will guide you through:

- Site name
- Domain name
- Site type
- Backend or root directory
- Automatic privilege elevation
- Validation
- Nginx reload

---

# Usage

## Reverse Proxy

```bash
ngxctl create reverse-proxy \
    --site-name my-api \
    --domain api.example.com \
    --port 3000
```

Using a custom backend URL:

```bash
ngxctl create reverse-proxy \
    --domain api.example.com \
    --port http://127.0.0.1:8080
```

Enable WebSockets:

```bash
ngxctl create reverse-proxy \
    --domain socket.example.com \
    --port 3000 \
    --websocket
```

---

## Static Website

```bash
ngxctl create static \
    --site-name my-site \
    --domain example.com \
    --root /var/www/my-site
```

SPA with a custom entrypoint:

```bash
ngxctl create static \
    --site-name my-app \
    --domain app.example.com \
    --root /var/www/app/dist \
    --entrypoint main.html \
    --spa
```

---

## PHP

```bash
ngxctl create php \
    --domain blog.example.com \
    --root /var/www/blog
```

---

# Site Management

List sites:

```bash
ngxctl list
```

Inspect a site:

```bash
ngxctl inspect my-site
```

Enable a site:

```bash
ngxctl enable my-site
```

Disable a site:

```bash
ngxctl disable my-site
```

---

# Nginx Operations

Validate:

```bash
ngxctl test
```

Reload:

```bash
ngxctl reload
```

Restart:

```bash
ngxctl restart
```

---

# Backup Management

Create a backup:

```bash
ngxctl backup create my-site
```

List backups:

```bash
ngxctl backup list
```

Restore:

```bash
ngxctl backup restore my-site
```

---

# Environment Variables

| Variable | Description | Default |
|-----------|-------------|---------|
| `NGXCTL_NGINX_DIR` | Base Nginx directory | `/etc/nginx` |
| `NGXCTL_SITES_AVAILABLE` | Sites Available | `/etc/nginx/sites-available` |
| `NGXCTL_SITES_ENABLED` | Sites Enabled | `/etc/nginx/sites-enabled` |
| `NGXCTL_CONF_D` | conf.d directory | `/etc/nginx/conf.d` |
| `NGXCTL_BACKUP_DIR` | Backup location | `~/.config/ngxctl/backups` |

---

# Design Principles

- Keep commands intuitive.
- Generate clean, readable configurations.
- Avoid unnecessary complexity.
- Never apply invalid configurations.
- Keep everything modular.
- Produce standard Nginx files.
- Allow manual editing.

---

# Example Workflow

Generate a configuration:

```bash
ngxctl create
```

Validate it:

```bash
ngxctl test
```

Reload Nginx:

```bash
ngxctl reload
```

---

# Contributing

```bash
git clone https://github.com/thexento/ngxctl.git
cd ngxctl

git checkout -b feature/my-feature

# Make your changes

git commit -m "Add my feature"
git push origin feature/my-feature
```

Open a Pull Request describing your changes.

---

# Frequently Asked Questions

### Does ngxctl replace Nginx?

No.

It generates and manages Nginx configuration files while Nginx continues serving traffic.

### Are generated configurations editable?

Yes.

Every generated file is a standard Nginx configuration that can be edited manually.

### Does ngxctl overwrite existing files?

Only when instructed. Backup snapshots are created before overwriting existing configurations.

### Which operating systems are supported?

Currently Linux systems running Nginx.

---

# License

This project is licensed under the MIT License.

See the **LICENSE** file for details.

---

<div align="center">

### Developed and maintained by **Xento**

<a href="https://github.com/thexento">GitHub</a>

⭐ If you find this project useful, consider giving it a star.

</div>
