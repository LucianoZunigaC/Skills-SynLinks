---
name: repo-documentation
description: "This skill should be used when structuring features with standard files, writing Google Style docstrings, documenting SQLAlchemy models with xd_ audit fields, and enriching FastAPI endpoints for OpenAPI."
metadata:
  author: aki-team
  version: 1.0.0
risk: safe
---

# Repository Documentation — aki-web-backend

## Purpose

Standard de documentación para que humanos y agentes de IA naveguen el codebase con mínima fricción. Aplica a toda feature en `src/features/`.

## When to Use This Skill

This skill should be used when:
- Creando la estructura básica de archivos para una nueva feature
- Escribiendo docstrings para métodos en repositorios o servicios (Google Style)
- Documentando modelos SQLAlchemy y sus campos de auditoría `xd_`
- Enriqueciendo endpoints de FastAPI con descripciones para Swagger/OpenAPI

## Instructions

### Step 1: Crear la estructura de 6 archivos por feature

Cada módulo en `src/features/{name}/` debe contener:

```
src/features/{feature_name}/
├── __init__.py
├── models.py          # Tablas SQLAlchemy
├── schemas.py         # Modelos Pydantic (Request/Response)
├── repositories.py    # Capa de persistencia
├── services.py        # Lógica de negocio
├── endpoints.py       # Rutas FastAPI
└── dependencies.py    # Inyección de dependencias
```

### Step 2: Escribir docstrings en formato Google Style

Todo método público en `repositories.py` y `services.py` debe incluir `Args`, `Returns` y `Raises`.

```python
async def save_form_values(
    user_id: str,
    values: list[CreateFormData],
) -> bool:
    """
    Persiste valores asociados a un formulario y periodo.

    Args:
        user_id: ID del usuario que registra la acción.
        values: Lista de schemas con los datos a persistir.

    Returns:
        True si la operación se completó exitosamente.

    Raises:
        SQLAlchemyError: Error de integridad en la base de datos.
    """
```

### Step 3: Documentar modelos SQLAlchemy con campos xd_

Incluir docstring de clase y documentar los campos de auditoría estándar.

```python
class Scenery(Base):
    """
    Representa un escenario de datos (Presupuesto, Real, etc.).

    Campos de auditoría:
    - xd_creation / xd_creationUser: Alta y usuario originador.
    - xd_lastUpdate / xd_lastUpdateUsr: Modificación y último editor.
    """
    __tablename__ = 'scenarios'
```

### Step 4: Enriquecer endpoints para OpenAPI

Usar `response_model`, `summary` y `description` en los decoradores de ruta.

```python
@router.get(
    "/history",
    response_model=list[FormHistory],
    summary="Listar historial de periodos",
    description="Retorna el historial de cambios del formulario activo."
)
async def get_history(service: FormServiceDep):
    return await service.get_history()
```

## Examples

- **Scenario**: Crear una nueva feature "alerts" desde cero.
- **Action**: Crear la carpeta `src/features/alerts/` con los 6 archivos, docstrings Google Style en `services.py` y `repositories.py`, y decoradores completos en `endpoints.py`.

- **Scenario**: Documentar un SP que se llama desde un repositorio.
- **Action**: Mencionar el nombre del SP en el docstring: `"""Obtiene datos vía sp_getFormHistory."""`

## Troubleshooting

- **Problem**: Swagger no muestra los tipos de respuesta.
- **Solution**: Verificar que `response_model` apunta al schema Pydantic correcto con `ConfigDict(from_attributes=True)`.

- **Problem**: El agente de IA modifica el archivo equivocado.
- **Solution**: Agregar un `README.md` en la carpeta de la feature describiendo su propósito.

## Validation Checklist

- [ ] Feature tiene los 6 archivos estándar + `__init__.py`
- [ ] Métodos públicos en repo y service tienen docstrings Google Style
- [ ] Endpoints incluyen `response_model`, `summary` y `description`
- [ ] Modelos SQLAlchemy tienen docstring y `__tablename__`
- [ ] Campos `xd_` documentados en los modelos
