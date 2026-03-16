# Skills-SynLinks

Repositorio de **Agent Skills** compartidas con una sola fuente de verdad (`.skills/`) y enlaces simbólicos para que cada agente (Cursor, Claude, Codex, GitHub) lea desde la carpeta que espera.

**Repositorio oficial:** https://github.com/LucianoZunigaC/Skills-SynLinks

## ¿Funciona en todos los sistemas?

| Comportamiento | Linux / macOS | Windows |
|----------------|---------------|---------|
| **Al hacer `git clone`** | Git crea los symlinks automáticamente si el repo los tiene guardados. | Necesita `git config core.symlinks true` y, a veces, permisos (Modo desarrollador o Admin). Si no, hay que ejecutar el script después del clone. |
| **Actualizar un skill** | Editas solo en `.skills/`; el resto son enlaces al mismo contenido, se “actualizan solos”. | Igual: un solo lugar (`.skills/`), el resto son enlaces. |
| **Crear los symlinks** | `./setup-symlinks.sh` (o `bash setup-symlinks.sh`). | `.\setup-symlinks.ps1` (PowerShell; puede requerir Admin o Modo desarrollador). |

Los symlinks son estándar de Git: si el repo **ya incluye** los enlaces (creados desde Linux, macOS o WSL y subidos con `git add` + `commit` + `push`), al hacer **clone en Linux o Mac los symlinks ya vienen hechos**. En Windows, o Git los recrea (con `core.symlinks true` y permisos) o ejecutas el script una vez después de clonar.

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
│   └── skills   → symlink a .skills
├── .cursor/
│   └── skills   → symlink a .skills
├── .codex/
│   └── skills   → symlink a .skills
├── .github/
│   └── skills   → symlink a .skills
├── setup-symlinks.sh            # Linux, macOS, WSL, Git Bash
├── setup-symlinks.ps1           # Windows (PowerShell)
└── README.md
```

Cualquier cambio en `.skills/` se refleja en `.claude/skills`, `.cursor/skills`, etc., porque son enlaces al mismo contenido (en todos los sistemas).

## Después de clonar: asegurar los symlinks

### Linux / macOS / WSL / Git Bash

```bash
chmod +x setup-symlinks.sh   # solo la primera vez
./setup-symlinks.sh
```

Si el repo ya trae symlinks guardados, a menudo **no hace falta** hacer nada; solo ejecuta el script si al clonar no ves enlaces o te salen carpetas copiadas.

### Windows (PowerShell)

En Windows los symlinks pueden requerir **Modo desarrollador** o **PowerShell como administrador**:

- **Modo desarrollador:** Configuración → Privacidad y seguridad → Para desarrolladores → Modo de desarrollador.
- O: clic derecho en PowerShell → “Ejecutar como administrador”.

En la raíz del repo:

```powershell
.\setup-symlinks.ps1
```

Recomendado para que Git no convierta symlinks en copias:

```powershell
git config core.symlinks true
```

## Cómo dejar el repo con symlinks ya hechos (clone listo)

Para que **al hacer `git clone` los symlinks vengan creados** donde el sistema lo permita:

1. **Crear los symlinks** en tu máquina:
   - **Linux / macOS / WSL:** `./setup-symlinks.sh`
   - **Windows:** `.\setup-symlinks.ps1` (con permisos si hace falta).
2. **Guardarlos en Git** (si tu Git tiene symlinks activos):
   ```bash
   git config core.symlinks true
   git add .claude/skills .cursor/skills .codex/skills .github/skills
   git commit -m "Añadir symlinks de skills"
   git push
   ```

A partir de ahí:

- **Linux / macOS:** al hacer `git clone`, los symlinks suelen aparecer solos.
- **Windows:** con `core.symlinks true` y permisos, Git puede crearlos al clonar; si no, basta con ejecutar `.\setup-symlinks.ps1` una vez después del clone.

## Resumen

| Pregunta | Respuesta |
|----------|-----------|
| ¿Funciona en Ubuntu, Mac y Windows? | Sí: mismo repo; en cada OS usas el script que toca (`.sh` o `.ps1`). |
| ¿Si actualizo un skill se actualiza en las demás carpetas? | Sí: solo editas en `.skills/`; el resto son enlaces a esa carpeta. |
| ¿El clone puede venir ya con los symlinks? | En Linux/Mac sí (si el repo tiene los symlinks guardados). En Windows a veces; si no, un solo `.\setup-symlinks.ps1` después del clone. |

Skills incluidas: create-rule, create-skill, create-subagent, update-cursor-settings, migrate-to-skills.
