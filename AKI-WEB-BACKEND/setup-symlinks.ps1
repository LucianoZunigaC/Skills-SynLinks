# Ejecutar desde esta carpeta (AKI-WEB-BACKEND): llama al script de la raíz del monorepo.
$parent = Split-Path $PSScriptRoot -Parent
$main = Join-Path $parent "setup-symlinks.ps1"
if (-not (Test-Path $main)) {
    Write-Error "No se encontró $main. Coloca este repo con setup-symlinks.ps1 en la carpeta padre de AKI-WEB-BACKEND."
    exit 1
}
& $main -MonorepoRoot $parent
