#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

python -m pip install --upgrade pip
if [ -f "researchAI/requirements.txt" ]; then
  python -m pip install -r researchAI/requirements.txt
fi
if [ -f "researchAI/tests/requirements-test.txt" ]; then
  python -m pip install -r researchAI/tests/requirements-test.txt
fi

pytest -q researchAI/tests/test_mcp_service.py
