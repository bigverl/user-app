# User App

A toy FastAPI 'user app' project. Built to learn JWT auth and async event system.

## Objectives

- **Structure**: Features - users, auth, events — each with distinct software layers
- **API layer**: users CRUD endpoints, wired through FastAPI DI
- **Domain layer**: `UserService` business logic and data access
- **Data**: In-memory only, no DB, no file
- **Exceptions**: Exceptions from the service layer translated to HTTP codes by one handler
- **Auth**: Password hashing via `bcrypt`, JWT via `PyJWT`
- **Testing**: In-memory only. Unit tests for each service. Component/contract tests for full http paths

## Running

```
uv run fastapi dev app/main.py
```

Docs at `/docs`.

## Development

```
just check           # lint, format, type-check
just test-unit        # service layer, no HTTP
just test-component    # full API through TestClient
```

`pre-commit install --hook-type pre-push` once after cloning — runs all of the above, plus a version-bump check, before every push.
