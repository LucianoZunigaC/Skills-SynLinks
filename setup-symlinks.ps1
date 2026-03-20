# Crea symlinks: AKI-WEB-BACKEND\.claude\skills, .cursor\skills, etc. -> AKI-WEB-BACKEND\.skills
#
# Funciona aunque ejecutes desde otra carpeta: usa la ubicación del script, el directorio actual o -MonorepoRoot.
# Windows: PowerShell como Administrador o Modo desarrollador.

param(
    # Raíz del monorepo (carpeta que contiene AKI-WEB-BACKEND). Si no la pasas, se detecta sola.
    [string]$MonorepoRoot = ""
)

$ErrorActionPreference = "Stop"

function Test-MonorepoRoot([string]$Path) {
    $skills = Join-Path $Path "AKI-WEB-BACKEND\.skills"
    return (Test-Path $skills)
}

# 1) Parámetro explícito
$resolved = $null
if ($MonorepoRoot) {
    $resolved = (Resolve-Path -LiteralPath $MonorepoRoot).Path
    if (-not (Test-MonorepoRoot $resolved)) {
        Write-Error "En '$resolved' no existe AKI-WEB-BACKEND\.skills. Revisa -MonorepoRoot."
        exit 1
    }
}
# 2) Script en la raíz del monorepo (junto a AKI-WEB-BACKEND)
elseif (Test-MonorepoRoot $PSScriptRoot) {
    $resolved = $PSScriptRoot
}
# 3) Script copiado dentro de AKI-WEB-BACKEND (misma carpeta que .skills)
elseif ((Test-Path (Join-Path $PSScriptRoot ".skills")) -and (Test-Path (Join-Path $PSScriptRoot "src"))) {
    $resolved = Split-Path $PSScriptRoot -Parent
    if (-not (Test-MonorepoRoot $resolved)) {
        Write-Error "No se pudo inferir el monorepo desde $($PSScriptRoot)"
        exit 1
    }
}
# 4) Directorio de trabajo actual es la raíz del monorepo
elseif (Test-MonorepoRoot (Get-Location).Path) {
    $resolved = (Get-Location).Path
}
else {
    Write-Host "No se encontró AKI-WEB-BACKEND\.skills." -ForegroundColor Red
    Write-Host ""
    Write-Host "Opciones:" -ForegroundColor Yellow
    Write-Host "  A) Ir a la raíz del repo (donde está la carpeta AKI-WEB-BACKEND) y ejecutar:" -ForegroundColor Cyan
    Write-Host "     .\setup-symlinks.ps1" -ForegroundColor White
    Write-Host "  B) Desde cualquier sitio, indicar la ruta:" -ForegroundColor Cyan
    Write-Host "     & 'C:\ruta\al\repo\setup-symlinks.ps1' -MonorepoRoot 'C:\ruta\al\repo'" -ForegroundColor White
    Write-Host "  C) Dentro de AKI-WEB-BACKEND usar el script pequeño:" -ForegroundColor Cyan
    Write-Host "     .\setup-symlinks.ps1" -ForegroundColor White
    Write-Host "     (el de esta carpeta llama al de la raíz)" -ForegroundColor Gray
    exit 1
}

$monorepoRoot = $resolved
$repoRoot = Join-Path $monorepoRoot "AKI-WEB-BACKEND"
$target = Join-Path $repoRoot ".skills"

Write-Host "Monorepo: $monorepoRoot" -ForegroundColor DarkGray
Write-Host "Backend:  $repoRoot" -ForegroundColor DarkGray

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

Write-Host "`nListo. Abre AKI-WEB-BACKEND como workspace en Cursor para .cursor/skills." -ForegroundColor Cyan
