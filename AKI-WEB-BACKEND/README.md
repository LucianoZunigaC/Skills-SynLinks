# Producto Backend API

## 🚀 Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env

# Ejecutar servidor
uvicorn src.main:app --reload
```

## 📚 Documentación API

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🏗️ Arquitectura

- **FastAPI** con arquitectura de capas
- **SQLAlchemy** para ORM
- **OAuth2 + JWT** para autenticación
- **Azure Blob Storage** para archivos

## 📁 Agent Skills (todo dentro de este backend)

- **`.skills/`** — fuente única; edita solo aquí.
- **`.claude/skills`**, **`.cursor/skills`**, **`.codex/skills`**, **`.github/skills`** — enlaces simbólicos a **`.skills/`** (mismo contenido para cada agente).

En la raíz del monorepo (carpeta padre) ejecuta **`setup-symlinks.ps1`** o **`setup-symlinks.sh`** para recrear los enlaces en Windows si hace falta.

**Cursor:** abre esta carpeta **`AKI-WEB-BACKEND`** como workspace para que cargue `.cursor/skills`.