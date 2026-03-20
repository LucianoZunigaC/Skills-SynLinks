# Skills-SynLinks

Repositorio de **Agent Skills** compartidas con una sola fuente de verdad en **`AKI-WEB-BACKEND/.skills/`** y enlaces simbólicos en la raíz (`.claude/skills`, `.cursor/skills`, etc.) para que cada agente lea desde la carpeta que espera.


## ¿Funciona en todos los sistemas?

| Comportamiento | Linux / macOS | Windows |
|----------------|---------------|---------|
| **Al hacer `git clone`** | Git crea los symlinks automáticamente si el repo los tiene guardados. | Necesita `git config core.symlinks true` y, a veces, permisos (Modo desarrollador o Admin). Si no, hay que ejecutar el script después del clone. |
| **Actualizar un skill** | Editas solo en `AKI-WEB-BACKEND/.skills/`; el resto son enlaces al mismo contenido. | Igual: un solo lugar (`AKI-WEB-BACKEND\.skills\`), el resto son enlaces. |
| **Crear los symlinks** | `./setup-symlinks.sh` (o `bash setup-symlinks.sh`). | `.\setup-symlinks.ps1` (PowerShell; puede requerir Admin o Modo desarrollador). |

Los symlinks son estándar de Git: si el repo **ya incluye** los enlaces (creados desde Linux, macOS o WSL y subidos con `git add` + `commit` + `push`), al hacer **clone en Linux o Mac los symlinks ya vienen hechos**. En Windows, o Git los recrea (con `core.symlinks true` y permisos) o ejecutas el script una vez después de clonar.

## Estructura

```
├── AKI-WEB-BACKEND/
│   └── .skills/                 # ← Fuente única: edita solo aquí
│       ├── database-interaction/
│       ├── repo-documentation/
│       ├── repo-rules/
│       └── stored-procedures/
├── .claude/
│   └── skills   → symlink a ../AKI-WEB-BACKEND/.skills
├── .cursor/
│   └── skills   → symlink a ../AKI-WEB-BACKEND/.skills
├── .codex/
│   └── skills   → symlink a ../AKI-WEB-BACKEND/.skills
├── .github/
│   └── skills   → symlink a ../AKI-WEB-BACKEND/.skills
├── setup-symlinks.sh            # Linux, macOS, WSL, Git Bash
├── setup-symlinks.ps1           # Windows (PowerShell)
└── README.md
```

Cualquier cambio en `AKI-WEB-BACKEND/.skills/` se refleja en `.claude/skills`, `.cursor/skills`, etc., porque son enlaces al mismo contenido (en todos los sistemas).

---

## Windows: paso a paso (git clone y symlinks listos)

Sigue estos pasos para clonar en Windows y dejar los enlaces simbólicos funcionando. Así, cuando edites algo en `AKI-WEB-BACKEND/.skills/`, se actualizará solo en ese sitio y el resto de carpetas (`.claude/skills`, `.cursor/skills`, etc.) lo verán automáticamente.

### 1. Activar soporte de symlinks en Git (una vez por equipo)

Abre **PowerShell** o **CMD** y ejecuta:

```powershell
git config --global core.symlinks true
```

Así Git no convertirá los enlaces en copias al clonar.

### 2. Dar permiso a Windows para crear symlinks (elegir una opción)

- **Opción A – Modo desarrollador (recomendado):**  
  **Configuración** → **Privacidad y seguridad** → **Para desarrolladores** → activar **Modo de desarrollador**.  
  No necesitas volver a hacer esto para cada clone.

- **Opción B – Sin Modo desarrollador:**  
  Abre PowerShell **como administrador** (clic derecho → “Ejecutar como administrador”) cuando vayas a clonar o cuando ejecutes el script del paso 4.

### 3. Clonar el repositorio

En la carpeta donde quieras el proyecto (por ejemplo `Documents` o `Proyectos`):

```powershell
cd C:\Users\TuUsuario\Documents
git clone https://github.com/LucianoZunigaC/Skills-SynLinks.git
cd Skills-SynLinks
```

Sustituye `TuUsuario` por tu usuario de Windows si hace falta.

### 4. Si los symlinks no se crearon al clonar, ejecutar el script

Comprueba si ya existen los enlaces:

```powershell
   Get-Item .claude\skills | Select-Object LinkType, Target
```

Si ves `LinkType: SymbolicLink` y `Target` apuntando a `AKI-WEB-BACKEND\.skills`, ya están listos y puedes saltar al paso 5.

Si no existen o son carpetas normales (no enlaces), en la raíz del repo (`Skills-SynLinks`) ejecuta:

```powershell
.\setup-symlinks.ps1
```

- Con **Modo desarrollador** activado: abre PowerShell normal.  
- Sin Modo desarrollador: abre PowerShell **como administrador**.

**Si `skills` aparece como ".symlink" o no puedes abrirlo en el Explorador:** el enlace que creó Git al clonar a veces no funciona como carpeta en Windows. En la raíz del repo, ejecuta `.\setup-symlinks.ps1` (como administrador o con Modo desarrollador). El script quita ese enlace y crea uno nuevo que apunta a `AKI-WEB-BACKEND\.skills`.

### 5. Comprobar que todo funciona

- Entra en `AKI-WEB-BACKEND\.skills\repo-rules\` y abre `SKILL.md`, cambia una línea y guarda.
- Abre `.claude\skills\repo-rules\SKILL.md` (o `.cursor\skills\repo-rules\SKILL.md`).  
  Debe mostrar **el mismo cambio** sin hacer nada más.

Si es así, los symlinks están bien: **solo editas en `AKI-WEB-BACKEND/.skills/` y las demás carpetas se actualizan solas**.

### Resumen rápido (Windows)

| Paso | Qué hacer |
|------|-----------|
| 1 | `git config --global core.symlinks true` |
| 2 | Activar Modo desarrollador **o** usar PowerShell como Admin cuando haga falta |
| 3 | `git clone ...` y `cd Skills-SynLinks` |
| 4 | Si no hay enlaces: `.\setup-symlinks.ps1` |
| 5 | Editar solo en `AKI-WEB-BACKEND/.skills/`; el resto se actualiza solo |

---

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
| ¿Si actualizo un skill se actualiza en las demás carpetas? | Sí: solo editas en `AKI-WEB-BACKEND/.skills/`; el resto son enlaces a esa carpeta. |
| ¿El clone puede venir ya con los symlinks? | En Linux/Mac sí (si el repo tiene los symlinks guardados). En Windows a veces; si no, un solo `.\setup-symlinks.ps1` después del clone. |

Skills incluidas (en `AKI-WEB-BACKEND/.skills/`): database-interaction, repo-documentation, repo-rules, stored-procedures.
