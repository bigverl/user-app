check:
    scripts/static_analysis.sh

test-unit:
    uv run pytest tests/unit || test $? -eq 5

test-component:
    uv run pytest tests/component || test $? -eq 5

check-version-bump:
    uv run python3 scripts/check_version_bump.py
