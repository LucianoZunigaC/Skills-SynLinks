# Script para crear los enlaces simbólicos (symlinks) de skills.
# Ejecutar desde la raíz del repo (carpeta Skills o Skills-SynLinks).
#
# En Windows: puede requerir "Ejecutar como administrador" O activar
# Modo desarrollador: Configuración > Privacidad y seguridad > Para desarrolladores > Modo de desarrollador

$ErrorActionPreference = "Stop"
$repoRoot = $PSScriptRoot
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
    # Si ya existe (enlace roto por Git o anterior), quitarlo para crear uno que funcione en Explorer
    if (Test-Path $link.Path) {
        try {
            $item = Get-Item $link.Path -Force -ErrorAction Stop
            $isLink = ($item.LinkType -eq 'SymbolicLink') -or ($item.LinkType -eq 'Junction') -or
                      (([System.IO.FileAttributes]::ReparsePoint -band $item.Attributes) -eq [System.IO.FileAttributes]::ReparsePoint)
            if ($isLink) {
                Remove-Item -LiteralPath $link.Path -Force -ErrorAction Stop
                Write-Host "Eliminado enlace anterior: $($link.Path)" -ForegroundColor Yellow
            } else {
                Write-Host "Ya existe (no es enlace): $($link.Path)" -ForegroundColor Yellow
                continue
            }
        } catch {
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
        Write-Host "Prueba: 1) Ejecutar PowerShell como Administrador, o 2) Activar Modo desarrollador en Windows." -ForegroundColor Cyan
    }
}

Write-Host "`nListo. Comprueba con: Get-ChildItem -Force .claude, .cursor, .codex, .github" -ForegroundColor Cyan
