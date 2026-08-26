#!/usr/bin/env bash

set -euo pipefail

cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."

if [[ ! -x .venv/bin/mkdocs ]]; then
  python3 -m venv .venv
  .venv/bin/python -m pip install --requirement requirements.txt
fi

exec .venv/bin/mkdocs serve "$@"