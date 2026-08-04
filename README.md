<div align="center">

# ngxctl

**A modern command-line utility for generating, managing, validating, and applying Nginx configurations.**

<p>

<a href="https://www.python.org/downloads/">
<img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</a>

<a href="https://nginx.org/">
<img src="https://img.shields.io/badge/Nginx-Supported-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="Nginx">
</a>

<a href="LICENSE">
<img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="MIT License">
</a>

<img src="https://img.shields.io/badge/Linux-Supported-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux">

<img src="https://img.shields.io/badge/CLI-Terminal-4D4D4D?style=for-the-badge&logo=gnubash&logoColor=white" alt="CLI">

</p>

*A cleaner way to work with Nginx.*

</div>

---

## Overview

`ngxctl` is an open-source command-line utility that simplifies the process of creating, managing, validating, and deploying Nginx configurations.

Whether you're deploying a personal project, hosting a production API, or setting up multiple virtual hosts on a VPS, `ngxctl` eliminates repetitive configuration work while keeping every generated file clean, readable, and fully editable.

Instead of manually creating server blocks, enabling sites, validating syntax, and reloading Nginx, `ngxctl` automates the workflow through a simple and intuitive command-line interface.

The goal isn't to replace Nginx.

The goal is to make working with Nginx faster, safer, and significantly less repetitive.

---

# Why ngxctl?

Working with Nginx often involves repeating the same workflow:

* Create a new configuration.
* Copy an old server block.
* Replace the domain.
* Replace the backend port.
* Enable the site.
* Test the configuration.
* Reload Nginx.

Repeat that enough times and it becomes tedious.

`ngxctl` automates those repetitive steps while still generating standard Nginx configuration files that you can edit manually whenever you need to.

---

# Features

## Configuration Generation

* Reverse proxy configuration
* Static website hosting
* Single Page Application (SPA) support
* PHP-FPM applications
* Docker reverse proxy templates
* WebSocket support
* SSL-ready templates
* HTTP → HTTPS redirects

---

## Supported Backends

| Backend           | Supported |
| ----------------- | :-------: |
| Node.js           |     ✓     |
| Express           |     ✓     |
| NestJS            |     ✓     |
| FastAPI           |     ✓     |
| Flask             |     ✓     |
| Django            |     ✓     |
| Go                |     ✓     |
| PHP-FPM           |     ✓     |
| Docker Containers |     ✓     |
| Static Websites   |     ✓     |
| React             |     ✓     |
| Vue               |     ✓     |
| Svelte            |     ✓     |

---

## Site Management

* Create new sites
* Enable existing sites
* Disable sites
* Delete sites
* List configured sites
* Inspect configurations
* Automatic symlink management

---

## Service Management

* Validate configurations using `nginx -t`
* Reload Nginx
* Restart Nginx
* Safe validation before reload

---

## Backup & Recovery

* Automatic snapshot creation
* Timestamped backups
* Restore previous configurations
* Backup listing
* Rollback support

---

# Installation

## Requirements

Before installing `ngxctl`, ensure you have:

* Python 3.12 or newer
* Nginx installed
* Linux-based operating system

---

## Install from PyPI

```bash
pip install ngxctl
```

---

## Install with pipx

```bash
pipx install git+https://github.com/thexento/ngxctl.git
```

---

## Install from Source

Clone the repository.

```bash
git clone https://github.com/thexento/ngxctl.git
```

Move into the project.

```bash
cd ngxctl
```

Create a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project.

```bash
pip install -e .
```

---

# Quick Start

Launch the interactive setup wizard.

```bash
ngxctl create
```

The wizard guides you through:

* Domain name
* Site type
* Backend configuration
* Output location
* Automatic validation
* Automatic reload

---

# Usage

## Reverse Proxy

```bash
ngxctl create reverse-proxy \
    --domain api.example.com \
    --port 3000
```

Custom backend URL.

```bash
ngxctl create reverse-proxy \
    --domain api.example.com \
    --proxy-pass http://127.0.0.1:8080
```

Enable WebSocket support.

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
    --domain example.com \
    --root /var/www/example
```

SPA Support.

```bash
ngxctl create static \
    --domain app.example.com \
    --root /var/www/app/dist \
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

List all sites.

```bash
ngxctl list
```

Inspect a site.

```bash
ngxctl inspect mysite
```

Enable a site.

```bash
ngxctl enable mysite
```

Disable a site.

```bash
ngxctl disable mysite
```

Delete a site.

```bash
ngxctl delete mysite
```

---

# Nginx Operations

Validate configuration.

```bash
ngxctl test
```

Reload Nginx.

```bash
ngxctl reload
```

Restart Nginx.

```bash
ngxctl restart
```

Display service status.

```bash
ngxctl status
```

---

# Backup Management

Create a backup.

```bash
ngxctl backup create mysite
```

List backups.

```bash
ngxctl backup list
```

Restore a backup.

```bash
ngxctl backup restore mysite
```

Delete a backup.

```bash
ngxctl backup delete mysite
```

---

# Environment Variables

| Variable                 | Description               | Default                      |
| ------------------------ | ------------------------- | ---------------------------- |
| `NGXCTL_NGINX_DIR`       | Base Nginx directory      | `/etc/nginx`                 |
| `NGXCTL_SITES_AVAILABLE` | Sites Available directory | `/etc/nginx/sites-available` |
| `NGXCTL_SITES_ENABLED`   | Sites Enabled directory   | `/etc/nginx/sites-enabled`   |
| `NGXCTL_CONF_D`          | conf.d directory          | `/etc/nginx/conf.d`          |
| `NGXCTL_BACKUP_DIR`      | Backup directory          | System Default               |

---

# Project Structure

```text
ngxctl/
├── commands/
├── helpers/
├── templates/
├── utils/
├── __init__.py
├── __main__.py
├── cli.py
└── generator.py
```

---

# Design Principles

`ngxctl` follows a few simple principles.

* Keep commands intuitive.
* Generate clean and readable configurations.
* Avoid unnecessary complexity.
* Never apply invalid configurations.
* Keep everything modular.
* Produce standard Nginx files.
* Allow manual editing at any time.

---

# Example Workflow

Generate a reverse proxy.

```bash
ngxctl create
```

Validate the generated configuration.

```bash
ngxctl test
```

Reload Nginx.

```bash
ngxctl reload
```

Done.

---

# Contributing

Contributions are welcome.

If you would like to improve the project:

```bash
git clone https://github.com/thexento/ngxctl.git

cd ngxctl

git checkout -b feature/my-feature

# Make your changes

git commit -m "Add my feature"

git push origin feature/my-feature
```

Then open a Pull Request describing your changes.

Please keep contributions focused, readable, and well documented.

---

# Frequently Asked Questions

### Does ngxctl replace Nginx?

No.

`ngxctl` generates and manages Nginx configuration files. Nginx itself remains responsible for serving traffic.

---

### Are generated configurations editable?

Yes.

Every generated configuration is a normal Nginx configuration file and can be modified manually.

---

### Does ngxctl modify existing files?

Only when instructed to do so.

Whenever possible, backup snapshots are created before overwriting configurations.

---

### Which operating systems are supported?

Currently, the primary target is Linux systems running Nginx.

---

# License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for more information.

---

<div align="center">

Developed and maintained by **Xento**

GitHub: https://github.com/thexento

If you find this project useful, consider giving it a star.

</div>
