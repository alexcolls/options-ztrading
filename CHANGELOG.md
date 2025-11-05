# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning (pre-1.0).

## [Unreleased]
### Added
- Roadmap/TODO section in README
- CONTRIBUTING.md and TODO.md scaffolding

### Changed
- N/A

### Fixed
- N/A

## [0.1.0] - 2025-11-05
### Added
- Poetry project setup with CLI entrypoint (Typer)
- Environment configuration via .env and .env.sample
- Polygon.io API client with retry/backoff
- Services for fetching tickers and options snapshots (concurrent)
- Comprehensive README with installation, usage, and financial warnings
- Improved .gitignore for venv, env, and data artifacts

### Removed
- Legacy sellingOptions directory and committed virtualenv files
