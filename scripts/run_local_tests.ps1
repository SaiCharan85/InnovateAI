$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

python -m pip install --upgrade pip
if (Test-Path 'researchAI/requirements.txt') {
    python -m pip install -r researchAI/requirements.txt
}
if (Test-Path 'researchAI/tests/requirements-test.txt') {
    python -m pip install -r researchAI/tests/requirements-test.txt
}

pytest -q researchAI/tests/test_mcp_service.py
