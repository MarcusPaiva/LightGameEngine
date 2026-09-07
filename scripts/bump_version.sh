#!/usr/bin/env bash
# Bump LightGameEngine's patch version (X.Y.Z -> X.Y.(Z+1)) in
# pyproject.toml, then commit and tag that change.
#
# Usage:
#   ./scripts/bump_version.sh          # bump, commit, and tag
#   ./scripts/bump_version.sh --force  # bump even with other uncommitted changes in the tree
#
# Only the new version number is printed on stdout (the last line);
# everything else goes to stderr. This lets other scripts capture the
# version cleanly, e.g.:
#   VERSION="$(./scripts/bump_version.sh)"
#
# This does NOT push the commit or the tag - review them, then push
# yourself (git push && git push --tags) when you're ready.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

FORCE=false
for arg in "$@"; do
  case "$arg" in
    --force) FORCE=true ;;
    *)
      echo "Unknown option: $arg" >&2
      echo "Usage: $0 [--force]" >&2
      exit 1
      ;;
  esac
done

if [ "$FORCE" = false ] && [ -n "$(git status --porcelain)" ]; then
  echo "Working tree has uncommitted changes - refusing to bump the version." >&2
  echo "Commit or stash your changes first, or re-run with --force." >&2
  exit 1
fi

CURRENT_VERSION="$(grep -m1 '^version' pyproject.toml | sed -E 's/version[[:space:]]*=[[:space:]]*"(.*)"/\1/')"
if [ -z "$CURRENT_VERSION" ]; then
  echo "Could not read the version from pyproject.toml." >&2
  exit 1
fi

IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"
if [ -z "${MAJOR:-}" ] || [ -z "${MINOR:-}" ] || [ -z "${PATCH:-}" ]; then
  echo "Could not parse version '$CURRENT_VERSION' as MAJOR.MINOR.PATCH." >&2
  exit 1
fi

NEW_VERSION="$MAJOR.$MINOR.$((PATCH + 1))"

# -i.bak works with both GNU sed (Linux/Git Bash) and BSD sed (macOS).
sed -i.bak -E "s/^version[[:space:]]*=[[:space:]]*\"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml
rm -f pyproject.toml.bak

git add pyproject.toml
# [skip ci] stops this commit from re-triggering the deploy workflow -
# both when pushed by CI itself and when pushed manually after a local
# deploy (see .github/workflows/deploy-pypi.yml).
git commit --quiet -m "chore: bump version to $NEW_VERSION [skip ci]"
git tag "v$NEW_VERSION"

echo "Bumped version: $CURRENT_VERSION -> $NEW_VERSION" >&2
echo "$NEW_VERSION"
