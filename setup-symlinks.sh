#!/usr/bin/env bash
# Crea symlinks dentro de AKI-WEB-BACKEND: .claude/skills, .cursor/skills, etc. -> .skills
# Ejecutar desde la raíz del monorepo (donde está este script y la carpeta AKI-WEB-BACKEND).

set -e
MONOREPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$MONOREPO_ROOT/AKI-WEB-BACKEND"
TARGET="$REPO_ROOT/.skills"

if [ ! -d "$TARGET" ]; then
  echo "Error: no se encuentra $TARGET" >&2
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
echo "Listo. Abre AKI-WEB-BACKEND como raíz del workspace en Cursor para usar .cursor/skills."
