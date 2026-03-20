#!/usr/bin/env bash
# Autónomo: ejecutar desde AKI-WEB-BACKEND (donde está este script).
set -e
REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
TARGET="$REPO_ROOT/.skills"
if [ ! -d "$TARGET" ]; then
  echo "ERROR: no existe $TARGET" >&2
  exit 1
fi
echo "Backend: $REPO_ROOT"
for dir in .claude .cursor .codex .github; do
  link_path="$REPO_ROOT/$dir/skills"
  parent="$REPO_ROOT/$dir"
  if [ -e "$link_path" ] || [ -L "$link_path" ]; then
    rm -f "$link_path"
    echo "Eliminado: $link_path"
  fi
  mkdir -p "$parent"
  ln -s "$TARGET" "$link_path"
  echo "OK: $link_path -> $TARGET"
done
echo "Listo."
