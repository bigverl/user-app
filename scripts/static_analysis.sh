#!/usr/bin/env bash

echo "--- ruff lint (autofix) ---"
uv run ruff check --fix . || true

echo ""
echo "--- ruff format ---"
uv run ruff format .

echo ""
echo "--- collecting non-auto-fixable issues ---"
: > .checks.txt
uv run ruff check . 2>&1 | tee .checks.txt
lint_exit=${PIPESTATUS[0]}
uv run ruff format --check . 2>&1 | tee -a .checks.txt
fmt_exit=${PIPESTATUS[0]}

echo ""
echo "--- pyright type check ---"
uv run pyright . 2>&1 | tee -a .checks.txt
type_exit=${PIPESTATUS[0]}

# write
if [ $lint_exit -ne 0 ] || [ $fmt_exit -ne 0 ] || [ $type_exit -ne 0 ]; then
    echo ""
    echo "--- remaining issues written to .checks.txt ---"
    exit 1
else
    echo ""
    echo "--- all clean ---"
    rm -f .checks.txt
    exit 0
fi
