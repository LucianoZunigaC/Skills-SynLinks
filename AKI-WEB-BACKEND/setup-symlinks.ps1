# Script AUTÓNOMO: ejecutar desde esta carpeta (AKI-WEB-BACKEND).
# Crea .claude\skills, .cursor\skills, .codex\skills, .github\skills -> .skills (misma carpeta).
#
# Requiere: Modo desarrollador en Windows O PowerShell como Administrador.

$ErrorActionPreference = "Continue"

# Siempre usamos la carpeta donde está ESTE archivo (AKI-WEB-BACKEND), no el directorio actual.
$repoRoot = $PSScriptRoot
$target = Join-Path $repoRoot ".skills"

Write-Host "=== setup-symlinks (AKI-WEB-BACKEND) ===" -ForegroundColor Cyan
Write-Host "Carpeta backend: $repoRoot" -ForegroundColor Gray

if (-not (Test-Path $target)) {
    Write-Host "ERROR: No existe la carpeta .skills aquí: $target" -ForegroundColor Red
    exit 1
}

$links = @(
    @{ Path = Join-Path $repoRoot ".claude\skills"; Target = $target }
    @{ Path = Join-Path $repoRoot ".cursor\skills"; Target = $target }
    @{ Path = Join-Path $repoRoot ".codex\skills"; Target = $target }
    @{ Path = Join-Path $repoRoot ".github\skills"; Target = $target }
)

$failed = $false
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
            Write-Host "No se pudo eliminar $($link.Path): $($_.Exception.Message)" -ForegroundColor Red
            $failed = $true
            continue
        }
    }
    try {
        New-Item -ItemType SymbolicLink -Path $link.Path -Target $link.Target -ErrorAction Stop | Out-Null
        Write-Host "OK: $($link.Path) -> $($link.Target)" -ForegroundColor Green
    } catch {
        Write-Host "ERROR al crear symlink: $($link.Path)" -ForegroundColor Red
        Write-Host "  $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "  Activa Modo desarrollador (Windows) o ejecuta PowerShell como Administrador." -ForegroundColor Yellow
        $failed = $true
    }
}

if ($failed) {
    Write-Host "`nTerminó con errores. Revisa permisos para crear symlinks." -ForegroundColor Red
    exit 1
}
Write-Host "`nListo. Comprueba: Get-Item .cursor\skills | Select-Object LinkType, Target" -ForegroundColor Cyan
