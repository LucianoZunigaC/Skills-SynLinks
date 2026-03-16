# Skills-SynLinks

Repositorio de **Agent Skills** compartidas con una sola fuente de verdad (`.skills/`) y enlaces simbólicos para que cada agente (Cursor, Claude, Codex, GitHub) lea desde la carpeta que espera.

## Estructura

```
├── .skills/                    # ← Fuente única: edita solo aquí
│   ├── create-rule/
│   │   └── SKILL.md
│   ├── create-skill/
│   ├── create-subagent/
│   ├── update-cursor-settings/
│   └── migrate-to-skills/
├── .claude/
│   └── skills   → symlink a ../.skills
├── .cursor/
│   └── skills   → symlink a ../.skills
├── .codex/
│   └── skills   → symlink a ../.skills
├── .github/
│   └── skills   → symlink a ../.skills
├── setup-symlinks.ps1
└── README.md
```

Cualquier cambio en `.skills/` se refleja automáticamente en `.claude/skills`, `.cursor/skills`, etc., porque son enlaces al mismo contenido.

## Crear el repositorio en GitHub

1. Ve a [github.com/new](https://github.com/new).
2. **Repository name:** `Skills-SynLinks`
3. **Owner:** tu usuario (`LucianoZunigaC`).
4. Opción: **Private** o **Public**.
5. No marques "Add a README" (ya tienes uno en este repo).
6. Clic en **Create repository**.

## Subir este proyecto a GitHub

Desde la carpeta del proyecto (donde está este README):

```powershell
git init
git config core.symlinks true
git add .
git commit -m "Initial commit: .skills + estructura y script de symlinks"
git branch -M main
git remote add origin https://github.com/LucianoZunigaC/Skills-SynLinks.git
git push -u origin main
```

Si no tienes `git config core.symlinks true`, en Windows Git puede convertir los symlinks en archivos normales al clonar.

## Después de clonar (o si aún no tienes symlinks)

En Windows, los symlinks suelen requerir **privilegios de administrador** o **Modo desarrollador**:

- **Modo desarrollador:** Configuración → Privacidad y seguridad → Para desarrolladores → **Modo de desarrollador** (recomendado).
- O ejecutar PowerShell **como administrador**.

Luego, en la raíz del repo:

```powershell
.\setup-symlinks.ps1
```

Eso crea:

- `.claude/skills` → `.skills`
- `.cursor/skills` → `.skills`
- `.codex/skills` → `.skills`
- `.github/skills` → `.skills`

Para que Git guarde estos enlaces en el repo (y al clonar se recreen), antes del primer commit con symlinks:

```powershell
git config core.symlinks true
```

Luego añade los symlinks y haz commit:

```powershell
git add .claude/skills .cursor/skills .codex/skills .github/skills
git commit -m "Añadir symlinks de skills"
git push
```

## Resumen

| Dónde | Qué hacer |
|-------|-----------|
| **Editar skills** | Solo en `.skills/` |
| **Crear repo en GitHub** | Manual en github.com, nombre `Skills-SynLinks` |
| **Subir código** | `git init`, `git config core.symlinks true`, `git add`, `commit`, `remote`, `push` |
| **Al clonar / sin symlinks** | Ejecutar `.\setup-symlinks.ps1` (con admin o Modo desarrollador) |

Skills incluidas: create-rule, create-skill, create-subagent, update-cursor-settings, migrate-to-skills (desde Cursor).
