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