#!/bin/bash

set -e

SCRIPT_PATH="${BASH_SOURCE[0]}"
SCRIPT_DIR="${SCRIPT_PATH%/*}"

if [[ "$SCRIPT_DIR" == "$SCRIPT_PATH" ]]; then
	SCRIPT_DIR='.'
fi

cd "$SCRIPT_DIR"
SCRIPT_DIR="$PWD"
REPO_ROOT="${SCRIPT_DIR%/*}"

if [[ -n "${PYTHON_BIN}" ]]; then
	PYTHON="$PYTHON_BIN"
elif [[ -x "$REPO_ROOT/.venv/bin/python" ]]; then
	PYTHON="$REPO_ROOT/.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
	PYTHON="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
	PYTHON="$(command -v python)"
else
	echo "No Python interpreter found" >&2
	exit 127
fi

"$PYTHON" ad.py
"$PYTHON" gfwlist.py
"$PYTHON" build_confs.py
"$PYTHON" build_lazy_confs.py
