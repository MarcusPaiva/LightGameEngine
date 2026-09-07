#!/usr/bin/env bash
# Build and publish LightGameEngine to PyPI (or TestPyPI).
#
# Usage:
#   ./scripts/deploy_pypi.sh                # bump patch version, run tests, build, confirm, upload to PyPI
#   ./scripts/deploy_pypi.sh --test         # upload to https://test.pypi.org instead
#   ./scripts/deploy_pypi.sh --skip-tests   # skip running the test suite first
#   ./scripts/deploy_pypi.sh --no-bump      # deploy the version already in pyproject.toml, unchanged
#   ./scripts/deploy_pypi.sh --yes          # don't ask for confirmation before uploading
#
# You can combine flags, e.g.: ./scripts/deploy_pypi.sh --test --yes
#
# Every run bumps the patch version (via bump_version.sh) and commits
# + tags that change locally, unless --no-bump is given. That commit
# and tag are not pushed automatically - push them yourself once
# you're happy with the release (git push && git push --tags).
#
# Credentials:
#   twine reads them from ~/.pypirc, or from the TWINE_USERNAME /
#   TWINE_PASSWORD environment variables. PyPI wants an API token, not
#   a normal password:
#       export TWINE_USERNAME=__token__
#       export TWINE_PASSWORD=pypi-xxxxxxxx...
#   Use a token starting with "pypi-" for PyPI, or the token from
#   https://test.pypi.org/manage/account/ for TestPyPI (--test).
#   If neither ~/.pypirc nor the env vars are set, twine will ask for
#   them interactively when it uploads.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

REPOSITORY="pypi"
SKIP_TESTS=false
ASSUME_YES=false
SKIP_BUMP=false

for arg in "$@"; do
  case "$arg" in
    --test) REPOSITORY="testpypi" ;;
    --skip-tests) SKIP_TESTS=true ;;
    --no-bump) SKIP_BUMP=true ;;
    --yes|-y) ASSUME_YES=true ;;
    *)
      echo "Unknown option: $arg" >&2
      echo "Usage: $0 [--test] [--skip-tests] [--no-bump] [--yes]" >&2
      exit 1
      ;;
  esac
done

# Prefer the project's own virtualenv if one exists.
if [ -x "$REPO_ROOT/.venv/Scripts/python.exe" ]; then
  PYTHON="$REPO_ROOT/.venv/Scripts/python.exe"   # Windows-style venv layout
elif [ -x "$REPO_ROOT/.venv/bin/python" ]; then
  PYTHON="$REPO_ROOT/.venv/bin/python"           # POSIX-style venv layout
else
  PYTHON="python"
fi

echo "==> Using Python: $("$PYTHON" --version) ($PYTHON)"

if [ "$SKIP_BUMP" = false ]; then
  echo "==> Bumping the package version..."
  VERSION="$("$REPO_ROOT/scripts/bump_version.sh")"
else
  echo "==> Skipping version bump (--no-bump given)."
  VERSION="$(grep -m1 '^version' pyproject.toml | sed -E 's/version[[:space:]]*=[[:space:]]*"(.*)"/\1/')"
fi
if [ -z "$VERSION" ]; then
  echo "Could not read the version from pyproject.toml." >&2
  exit 1
fi
echo "==> Package version: $VERSION"
echo "==> Target repository: $REPOSITORY"

echo "==> Making sure build and twine are installed..."
"$PYTHON" -m pip install --quiet --upgrade build twine

if [ "$SKIP_TESTS" = false ]; then
  echo "==> Running the test suite..."
  "$PYTHON" -m pytest -q
else
  echo "==> Skipping tests (--skip-tests given)."
fi

echo "==> Cleaning old build artifacts..."
rm -rf dist build ./*.egg-info

echo "==> Building the sdist and wheel..."
"$PYTHON" -m build

echo "==> Checking the built distribution..."
"$PYTHON" -m twine check dist/*

if [ "$ASSUME_YES" = false ]; then
  read -r -p "Upload LightGameEngine $VERSION to $REPOSITORY? [y/N] " REPLY
  case "$REPLY" in
    [yY]|[yY][eE][sS]) ;;
    *) echo "Aborted."; exit 1 ;;
  esac
fi

if [ "$REPOSITORY" = "testpypi" ]; then
  "$PYTHON" -m twine upload --repository testpypi dist/*
else
  "$PYTHON" -m twine upload dist/*
fi

echo "==> Done. Published version $VERSION to $REPOSITORY."
