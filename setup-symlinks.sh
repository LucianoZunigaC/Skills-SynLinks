#!/usr/bin/env bash
# Crea enlaces simbólicos para que .claude/skills, .cursor/skills, etc. apunten a .skills
# Uso: ejecutar desde la raíz del repo (Linux, macOS, WSL, Git Bash)
# Ejemplo: ./setup-symlinks.sh  o  bash setup-symlinks.sh

set -e
REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
TARGET="$REPO_ROOT/AKI-WEB-BACKEND/.skills"

if [ ! -d "$TARGET" ]; then
  echo "Error: no se encuentra la carpeta AKI-WEB-BACKEND/.skills en $REPO_ROOT" >&2
  exit 1
fi

for dir in .claude .cursor .codex .github; do
  link_path="$REPO_ROOT/$dir/skills"
  parent="$REPO_ROOT/$dir"
  if [ -e "$link_path" ]; then
    echo "Ya existe: $link_path"
    continue
  fi
  mkdir -p "$parent"
  ln -s "$TARGET" "$link_path"
  echo "Creado: $link_path -> $TARGET"
done

echo ""
echo "Listo. Comprueba con: ls -la .claude .cursor .codex .github"
