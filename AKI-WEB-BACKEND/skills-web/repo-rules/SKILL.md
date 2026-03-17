---
name: repo-rules
description: "This skill should be used when applying Python 3.10+ type hints, configuring Pydantic V2 with camelCase aliases, defining xd_ audit fields in models, or setting up dependency injection with Annotated in aki-web-backend."
metadata:
  author: aki-team
  version: 1.0.0
risk: safe
---

# Repository Rules — aki-web-backend

## Purpose

Reglas no negociables de desarrollo para el backend. El incumplimiento es motivo de rechazo en Code Review.

## When to Use This Skill

This skill should be used when:
- Escribiendo código Python nuevo (requiere type hints explícitos 3.10+)
- Definiendo schemas de respuesta/petición en Pydantic V2
- Diseñando modelos persistentes en SQLAlchemy
- Inyectando dependencias en rutas de FastAPI
- Nombrando clases, funciones o constantes

## Instructions

### Step 1: Aplicar Type Hints en Python 3.10+

Todos los argumentos y retornos deben tener tipo explícito.
Usar `|` para uniones y `list[]` / `dict[]` para colecciones.

```python
# Correcto
async def get_by_code(code: str) -> Form | None:
    ...

# Rechazado
from typing import Optional, List
async def get_by_code(code) -> Optional[Form]:
    ...
```

### Step 2: Configurar Pydantic V2 con aliases

Todo schema de API debe usar `ConfigDict` y `Field(alias=)` para compatibilidad con el frontend (camelCase).

```python
from pydantic import BaseModel, Field, ConfigDict

class FormBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )

    form_code: str = Field(..., alias="formCode")
    short_name: str = Field(..., alias="shortName")
    xd_creation: datetime = Field(..., alias="created", exclude=True)
```

### Step 3: Incluir campos de auditoría xd_ en modelos

Todo modelo SQLAlchemy de entidad persistente debe tener estos 5 campos:

| Campo | Tipo SQL | Propósito |
|---|---|---|
| `status` | `CHAR(1)` | 'A' activo, 'I' inactivo |
| `xd_creation` | `DateTime` | Fecha de creación |
| `xd_creation_user` | `String(100)` | Usuario creador |
| `xd_last_update` | `DateTime` | Fecha de última modificación |
| `xd_last_update_user` | `String(100)` | Último usuario en modificar |

### Step 4: Usar Annotated para dependencias

Definir tipos de dependencia reutilizables en `dependencies.py`.

```python
from typing import Annotated
from fastapi import Depends

FormRepoDep = Annotated[FormRepository, Depends(get_form_repository)]
FormServiceDep = Annotated[FormService, Depends(get_form_service)]

# En endpoints.py
@router.get("/{form_id}")
async def read_form(form_id: int, service: FormServiceDep) -> FormBase:
    return await service.get(form_id)
```

### Step 5: Seguir convenciones de nombrado

| Elemento | Convención | Ejemplo |
|---|---|---|
| Clases | `PascalCase` | `FormRepository` |
| Funciones | `snake_case` | `get_form_by_id` |
| Constantes | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| API JSON | `camelCase` (via alias) | `"formCode"` |

## Examples

- **Scenario**: Crear un nuevo schema Pydantic para una entidad "Group".
- **Action**: Definir `GroupBase(BaseModel)` con `ConfigDict(populate_by_name=True, from_attributes=True)`, campos con `Field(..., alias="camelCase")`, y excluir campos `xd_` con `exclude=True`.

- **Scenario**: Agregar una dependencia para un nuevo servicio.
- **Action**: Crear `GroupServiceDep = Annotated[GroupService, Depends(get_group_service)]` en `dependencies.py`, usarla como tipo en el endpoint.

## Troubleshooting

- **Problem**: Frontend recibe campos en `snake_case` en vez de `camelCase`.
- **Solution**: Verificar que el schema tiene `Field(..., alias="camelCase")` y que `populate_by_name=True` está configurado.

- **Problem**: `model_validate()` falla al cargar desde ORM.
- **Solution**: Confirmar que `from_attributes=True` está en el `ConfigDict`.

- **Problem**: `field_validator` no se ejecuta.
- **Solution**: Usar el decorador `@field_validator('campo', mode='before')` con `@classmethod`.

## Validation Checklist

- [ ] Argumentos y retornos con Type Hints (`str | None`, no `Optional`)
- [ ] Schemas Pydantic con `ConfigDict(populate_by_name=True, from_attributes=True)`
- [ ] Aliases `camelCase` en campos que viajan al frontend
- [ ] Campos `xd_` presentes en todo modelo persistente
- [ ] Dependencias usan `Annotated[Type, Depends()]`
- [ ] Naming: `PascalCase` clases, `snake_case` funciones
