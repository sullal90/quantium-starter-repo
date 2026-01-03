#!/usr/bin/env bash
# Minimal test runner script for CI / local use.
# - tries to activate a virtualenv if found (.venv, venv, env)
# - runs pytest if available, otherwise falls back to the project's
#   `scripts/run_tests_no_pytest.py` runner
# - exits with 0 on success, 1 on any failure

set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[run_tests] Project root: $ROOT_DIR"

# Try to activate a virtualenv if present (several common names)
activate_found=0
for d in ".venv" "venv" "env"; do
  ACT="${ROOT_DIR}/${d}/bin/activate"
  if [ -f "$ACT" ]; then
    # shellcheck source=/dev/null
    echo "[run_tests] Activating virtualenv: ${d}"
    # shellcheck disable=SC1090
    source "$ACT"
    activate_found=1
    break
  fi
done

if [ "$activate_found" -eq 0 ]; then
  echo "[run_tests] No virtualenv activation script found (.venv/venv/env). Continuing with system Python."
fi

# Run tests: prefer pytest, otherwise fallback to the project's no-pytest runner
if command -v pytest >/dev/null 2>&1; then
  echo "[run_tests] Running tests with pytest"
  pytest -q
  rc=$?
else
  echo "[run_tests] pytest not found, running fallback runner"
  python3 "${ROOT_DIR}/scripts/run_tests_no_pytest.py"
  rc=$?
fi

if [ "$rc" -eq 0 ]; then
  echo "[run_tests] All tests passed"
  exit 0
else
  echo "[run_tests] Tests failed (exit code: $rc)"
  exit 1
fi
