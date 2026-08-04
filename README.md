# ngxctl

A modern Python CLI for generating, managing, and validating Nginx configurations.

`ngxctl` is designed to simplify common Nginx workflows. Instead of repeatedly copying configuration snippets or manually editing server blocks, you can generate, validate, and manage configurations through a straightforward command-line interface.

The project focuses on producing clean, readable configurations while automating repetitive tasks such as testing and reloading Nginx.

> **Status:** Active development. Features and commands may evolve until the first stable release.

---

# Features

## Current

* Generate Nginx configurations
* Reverse proxy configuration
* Static website configuration
* Interactive command-line interface
* Template-based configuration generation

## Planned

* React & Vue support
* Node.js application templates
* Python (Flask, Django, FastAPI) templates
* PHP support
* Docker reverse proxy templates
* SSL configuration
* HTTP to HTTPS redirects
* Configuration validation
* Reload and restart Nginx
* Enable and disable sites
* Configuration backup and restore
* Plugin system
* Custom templates

---

# Installation

## PyPI

Coming soon.

```bash
pip install ngxctl
```

---

## Development

Clone the repository.

```bash
git clone https://github.com/<your-username>/ngxctl.git
```

Move into the project.

```bash
cd ngxctl
```

Create a virtual environment.

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install the project.

```bash
pip install -e .
```

---

# Usage

Create a new configuration.

```bash
ngxctl create
```

Validate the current Nginx configuration.

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

Enable a site.

```bash
ngxctl enable mysite
```

Disable a site.

```bash
ngxctl disable mysite
```

List configurations.

```bash
ngxctl list
```

Inspect a configuration.

```bash
ngxctl inspect mysite
```

---

# Example Workflow

Generate a reverse proxy configuration.

```bash
ngxctl create
```

Validate the generated configuration.

```bash
ngxctl test
```

Reload Nginx after successful validation.

```bash
ngxctl reload
```

---

# Project Structure

```text
ngxctl/
├── commands/
├── helpers/
├── templates/
├── utils/
├── cli.py
├── generator.py
├── __main__.py
└── __init__.py
```

---

# Design Principles

The project follows a few simple principles.

* Keep the interface simple.
* Generate readable configurations.
* Avoid unnecessary complexity.
* Validate configurations before applying them.
* Build features incrementally.
* Keep the codebase modular and easy to extend.

---

# Contributing

Contributions are welcome.

If you'd like to improve the project:

```bash
git fork
git clone <your-fork>
cd ngxctl
```

Create a new branch.

```bash
git checkout -b feature/my-feature
```

Commit your changes.

```bash
git commit -m "Add my feature"
```

Push your branch.

```bash
git push origin feature/my-feature
```

Then open a Pull Request.

---

# Roadmap

* [ ] Reverse proxy generator
* [ ] Static website generator
* [ ] React support
* [ ] Vue support
* [ ] Node.js templates
* [ ] Python templates
* [ ] PHP templates
* [ ] Docker templates
* [ ] SSL support
* [ ] HTTP to HTTPS redirects
* [ ] Configuration validation
* [ ] Reload and restart Nginx
* [ ] Enable and disable sites
* [ ] Backup and restore
* [ ] Configuration inspector
* [ ] Plugin support

---

# License

This project is licensed under the MIT License.

See the `LICENSE` file for details.
