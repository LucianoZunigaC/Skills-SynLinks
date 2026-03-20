#!/usr/bin/env bash
# Crea symlinks dentro de AKI-WEB-BACKEND. Detecta la raíz del monorepo automáticamente.
# Uso: ./setup-symlinks.sh   o   MONOREPO_ROOT=/ruta ./setup-symlinks.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -n "${MONOREPO_ROOT:-}" ]; then
  REPO_ROOT="$MONOREPO_ROOT/AKI-WEB-BACKEND"
elif [ -d "$SCRIPT_DIR/AKI-WEB-BACKEND/.skills" ]; then
  REPO_ROOT="$SCRIPT_DIR/AKI-WEB-BACKEND"
elif [ -d "$SCRIPT_DIR/.skills" ] && [ -d "$SCRIPT_DIR/src" ]; then
  REPO_ROOT="$SCRIPT_DIR"
elif [ -d "$(pwd)/AKI-WEB-BACKEND/.skills" ]; then
  REPO_ROOT="$(pwd)/AKI-WEB-BACKEND"
else
  echo "No se encontró AKI-WEB-BACKEND/.skills. Opciones:" >&2
  echo "  - Ejecutar desde la raíz del monorepo (junto a AKI-WEB-BACKEND)" >&2
  echo "  - MONOREPO_ROOT=/ruta/al/monorepo ./setup-symlinks.sh" >&2
  echo "  - Desde AKI-WEB-BACKEND: ./setup-symlinks.sh (script pequeño en esa carpeta)" >&2
  exit 1
fi

TARGET="$REPO_ROOT/.skills"
if [ ! -d "$TARGET" ]; then
  echo "Error: no existe $TARGET" >&2
  exit 1
fi

echo "Backend: $REPO_ROOT"

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
echo "Listo. Abre AKI-WEB-BACKEND como raíz del workspace en Cursor."
