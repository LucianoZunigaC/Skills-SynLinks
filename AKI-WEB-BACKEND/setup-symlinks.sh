#!/usr/bin/env bash
# Ejecutar desde AKI-WEB-BACKEND
DIR="$(cd "$(dirname "$0")" && pwd)"
export MONOREPO_ROOT="$(cd "$DIR/.." && pwd)"
exec "$MONOREPO_ROOT/setup-symlinks.sh"
