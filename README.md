# r4a8h08
![PyPI version](https://img.shields.io/pypi/v/r4a8h08.svg)

Library to control the R4A8H08 Modbus IO expansion module.

* [GitHub](https://github.com/supermete/r4a8h08/) | [PyPI](https://pypi.org/project/r4a8h08/) | [Documentation](https://supermete.github.io/r4a8h08/)
* Created by [Rodolphe Mete Soyding](https://soyding.com) | GitHub [@supermete](https://github.com/supermete) | PyPI [@supermete](https://pypi.org/user/supermete/)
* MIT License

## Features

* TODO

## Documentation

Documentation is built with [Zensical](https://zensical.org/) and deployed to GitHub Pages.

* **Live site:** https://supermete.github.io/r4a8h08/
* **Preview locally:** `just docs-serve` (serves at http://localhost:8000)
* **Build:** `just docs-build`

API documentation is auto-generated from docstrings using [mkdocstrings](https://mkdocstrings.github.io/).

Docs deploy automatically on push to `main` via GitHub Actions. To enable this, go to your repo's Settings > Pages and set the source to **GitHub Actions**.

## Development

To set up for local development:

```bash
# Clone your fork
git clone git@github.com:your_username/r4a8h08.git
cd r4a8h08

# Install in editable mode with live updates
uv tool install --editable .
```

This installs the CLI globally but with live updates - any changes you make to the source code are immediately available when you run `r4a8h08`.

Run tests:

```bash
uv run pytest
```

Run quality checks (format, lint, type check, test):

```bash
just qa
```

## Author

r4a8h08 was created in 2026 by Rodolphe Mete Soyding.

Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.

