# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-23

### Added
- FastAPI project skeleton (`main.py`)
- `pre-commit`-managed pre-push pipeline (`.pre-commit-config.yaml`): lint/format/type-check, unit tests, component tests, and a version-bump check
- `scripts/static_analysis.sh` for lint/format/type-check, wired to `just check`
- `scripts/check_version_bump.py` — fails if `pyproject.toml`'s version isn't greater than `origin/main`'s
- `just check`, `just test-unit`, `just test-component`, `just check-version-bump` recipes
- `tests/unit/`, `tests/component/` structure, ready for the users module
