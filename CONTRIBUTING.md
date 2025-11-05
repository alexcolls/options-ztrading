# Contributing

Thank you for considering contributing!

## Getting started

- Use Poetry for dependency management.
- Copy `.env.sample` to `.env` and set `POLYGON_API_KEY`.
- Install deps: `poetry install`
- Run CLI: `poetry run options --help`

## Development workflow

- Lint/format: `poetry run ruff options_ztrading/` and `poetry run black options_ztrading/`
- Tests: `poetry run pytest`
- Keep changes small and focused (commit by feature).

## Commit style

- Use short, descriptive messages with an emoji prefix, e.g.:
  - ✨ feature, 🐛 fix, 📝 docs, 🧹 chore, ♻️ refactor, ✅ tests, 🔧 config

## Pull requests

- Target `dev` branch.
- Ensure CI (lint/tests) pass locally.
- Update README and CHANGELOG when user-facing behavior changes.

## Code style

- Prefer explicitness and type hints where helpful.
- Avoid example scripts; extend existing utilities/clients.
- Use absolute paths in docs/config where relevant.
