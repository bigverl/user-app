#!/usr/bin/env python3
"""Fail if pyproject.toml's version isn't greater than origin/main's."""

import subprocess
import sys
import tomllib


def read_version(ref: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{ref}:pyproject.toml"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return ""
    return tomllib.loads(result.stdout)["project"]["version"]


def parse(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def main() -> int:
    subprocess.run(["git", "fetch", "origin", "main", "--quiet"], check=False)

    local_version = read_version("HEAD")
    if not local_version:
        print("error: could not read version from HEAD:pyproject.toml", file=sys.stderr)
        return 1

    remote_version = read_version("origin/main")
    if not remote_version:
        print(f"no origin/main to compare against, version {local_version} OK")
        return 0

    if parse(local_version) > parse(remote_version):
        print(f"version bump OK: {remote_version} -> {local_version}")
        return 0

    print(
        f"error: pyproject.toml version ({local_version}) is not greater than "
        f"origin/main's ({remote_version}) - bump the version before pushing",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
