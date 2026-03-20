# Script para crear los enlaces simbólicos de skills dentro de AKI-WEB-BACKEND.
# Ejecutar desde la raíz del monorepo (donde está esta carpeta y AKI-WEB-BACKEND).
#
# Windows: PowerShell como Administrador o Modo desarrollador activado.

$ErrorActionPreference = "Stop"
$monorepoRoot = $PSScriptRoot
$repoRoot = Join-Path $monorepoRoot "AKI-WEB-BACKEND"
$target = Join-Path $repoRoot ".skills"

if (-not (Test-Path $target)) {
    Write-Error "No se encuentra la carpeta .skills en $repoRoot"
    exit 1
}

$links = @(
    @{ Path = Join-Path $repoRoot ".claude\skills"; Target = $target }
    @{ Path = Join-Path $repoRoot ".cursor\skills"; Target = $target }
    @{ Path = Join-Path $repoRoot ".codex\skills"; Target = $target }
    @{ Path = Join-Path $repoRoot ".github\skills"; Target = $target }
)

foreach ($link in $links) {
    $dir = Split-Path $link.Path -Parent
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    if (Test-Path $link.Path) {
        try {
            Remove-Item -LiteralPath $link.Path -Force -ErrorAction Stop
            Write-Host "Eliminado: $($link.Path)" -ForegroundColor Yellow
        } catch {
            if ($_.Exception.Message -match "no está vacío|not empty|directory") {
                Write-Host "Omitido (carpeta con contenido): $($link.Path)" -ForegroundColor Yellow
                continue
            }
            Write-Host "No se pudo eliminar $($link.Path): $_" -ForegroundColor Red
            Write-Host "Ejecuta PowerShell como Administrador o activa Modo desarrollador." -ForegroundColor Cyan
            continue
        }
    }
    try {
        New-Item -ItemType SymbolicLink -Path $link.Path -Target $link.Target | Out-Null
        Write-Host "Creado: $($link.Path) -> $($link.Target)" -ForegroundColor Green
    } catch {
        Write-Host "Error creando $($link.Path): $_" -ForegroundColor Red
        Write-Host "Prueba: PowerShell como Administrador o Modo desarrollador." -ForegroundColor Cyan
    }
}

Write-Host "`nListo. Skills en AKI-WEB-BACKEND\.skills; enlaces en AKI-WEB-BACKEND\.claude\skills, etc." -ForegroundColor Cyan
Write-Host "Nota: abre la carpeta AKI-WEB-BACKEND como raíz del workspace en Cursor para que use .cursor/skills." -ForegroundColor Cyan
