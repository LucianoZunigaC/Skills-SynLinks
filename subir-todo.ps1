# Ejecuta este script para subir todo a LucianoZunigaC/Skills-SynLinks
# Si falla con "index.lock": cierra Cursor/VS Code, borra .git\index.lock y vuelve a ejecutar.

$ErrorActionPreference = "Stop"
$repo = "c:\Users\lucia\Documents\Skills"
Set-Location $repo

# Quitar lock si quedó de un proceso anterior
$lock = Join-Path $repo ".git\index.lock"
if (Test-Path $lock) {
    Remove-Item $lock -Force
    Write-Host "Eliminado index.lock" -ForegroundColor Yellow
}

# No commitear la "eliminación" de los symlinks (Windows no los ve)
git restore --staged .claude/skills .cursor/skills .codex/skills .github/skills 2>$null

# Añadir este script y antigravity (antigravity tiene muchos archivos, puede tardar)
git add subir-todo.ps1 2>$null
Write-Host "Añadiendo antigravity-awesome-skills (puede tardar)..." -ForegroundColor Cyan
git add antigravity-awesome-skills/ 2>$null

# Commit y push
git commit -m "Subir todo: AKI-WEB-BACKEND, skills-web, antigravity-awesome-skills"
if ($LASTEXITCODE -eq 0) {
    git push origin main
    Write-Host "Listo. Todo subido a https://github.com/LucianoZunigaC/Skills-SynLinks" -ForegroundColor Green
} else {
    Write-Host "Commit falló (quizá nada nuevo). Estado:" -ForegroundColor Yellow
    git status -s
}
