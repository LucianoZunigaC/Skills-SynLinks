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

## 📁 Agent Skills (en este repo)

Las skills del proyecto están en **`.skills/`** (dentro de esta carpeta `AKI-WEB-BACKEND`). En la raíz del monorepo, `.claude/skills`, `.cursor/skills`, etc. son **enlaces simbólicos** a `AKI-WEB-BACKEND/.skills`: edita solo ahí y los agentes verán los mismos archivos.