# ngxctl

A command-line tool for generating, managing, and validating Nginx configurations.

`ngxctl` is built to simplify the repetitive parts of working with Nginx. Whether you're setting up a reverse proxy, serving a static website, or deploying an application, it helps you generate clean configurations, validate them, and safely apply changes without manually writing the same boilerplate every time.

The goal is simple: spend less time writing configuration files and more time building your applications.

> **Status:** This project is currently under active development. Features and commands may change until the first stable release.

---

## Features

### Current

* Generate Nginx configuration files
* Reverse proxy configuration generator
* Interactive command-line interface
* Template-based configuration generation

### Planned

* Static website templates
* React & Vue support
* Node.js application templates
* Python (Flask, Django, FastAPI) templates
* PHP support
* Docker reverse proxy templates
* SSL configuration
* HTTP to HTTPS redirects
* Configuration validation (`nginx -t`)
* Reload and restart Nginx
* Enable and disable sites
* Configuration inspection
* Backup and restore
* Custom templates

---

## Installation

### From PyPI

Coming soon.

```bash
pip install ngxctl
```

### Development

Clone the repository.

```bash
git clone https://github.com/thexento/ngxctl.git
```

Move into the project.

```bash
cd ngxctl
```

Create a virtual environment.

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install the project in editable mode.

```bash
pip install -e .
```

---

## Usage

Generate a new configuration.

```bash
ngxctl create
```

Validate the current Nginx configuration.

```bash
ngxctl test
```

Reload Nginx after a successful validation.

```bash
ngxctl reload
```

Restart the Nginx service.

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

List available configurations.

```bash
ngxctl list
```

Inspect a configuration.

```bash
ngxctl inspect mysite
```

---

## Example Workflow

Create a reverse proxy.

```bash
ngxctl create
```

Validate the generated configuration.

```bash
ngxctl test
```

If the configuration is valid, reload Nginx.

```bash
ngxctl reload
```

---

## Project Structure

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

## Contributing

Contributions are always welcome.

If you have an idea, find a bug, or would like to improve the project, feel free to open an issue or submit a pull request.

Clone your fork.

```bash
git clone <your-fork-url>
```

Create a feature branch.

```bash
git checkout -b feature/my-feature
```

Commit your changes.

```bash
git commit -m "Describe your changes"
```

Push the branch.

```bash
git push origin feature/my-feature
```

Then open a Pull Request.

---

## License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.
