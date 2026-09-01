# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-08-31

### Added
- Password hashing/verification via `bcrypt` and `pwdlib`
- JWT issuance and verification via `PyJWT`
- `POST /token` login endpoint
- `app/config.py` — `.env` settings loading
- Split role changes into their own admin-gated endpoint (`PATCH /users/{user_id}/role`)
- Unit tests for `security.py`/`dependencies.py`
- Component tests for the login flow and the role change guard

## [0.2.0] - 2026-08-30

### Added
- `User` Pydantic models
- In-memory seed data
- `UserService` service layer - domain-driven design CRUD.
- API layer CRUD with DI (`get_user_service`)
- Password hashing via `bcrypt`
- UserRole change guard on 'update user' requires admin role
- Exception handler in `main.py`
- Unit tests for `UserService`
- Component tests for full user module API path 

## [0.1.0] - 2026-08-23

### Added
- FastAPI project skeleton (`main.py`)
- `pre-commit`-managed pre-push pipeline (`.pre-commit-config.yaml`): lint/format/type-check, unit tests, component tests, and a version-bump check
- `scripts/static_analysis.sh` for lint/format/type-check, wired to `just check`
- `scripts/check_version_bump.py` — fails if `pyproject.toml`'s version isn't greater than `origin/main`'s
- `just check`, `just test-unit`, `just test-component`, `just check-version-bump` recipes
- `tests/unit/`, `tests/component/` structure, ready for the users module
