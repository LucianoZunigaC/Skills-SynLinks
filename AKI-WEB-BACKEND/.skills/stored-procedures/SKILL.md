---
name: stored-procedures
description: "This skill should be used when calling SQL Server Stored Procedures using sqlalchemy.text(), handling CursorResult, mapping xd_ audit parameters, and enforcing [dbo] schema usage in repositories."
metadata:
  author: aki-team
  version: 1.0.0
risk: safe
---

# Stored Procedures — aki-web-backend

## Purpose

Standard para llamadas a Stored Procedures de SQL Server usando SQLAlchemy 2.0. Toda llamada a SP debe vivir exclusivamente en `repositories.py` de la feature correspondiente.

## When to Use This Skill

This skill should be used when:
- Ejecutando rutinas almacenadas (Stored Procedures) en SQL Server
- Mapeando parámetros y resultados de SPs hacia diccionarios en Python
- Implementando SPs de lectura (SELECT) o de escritura (INSERT/UPDATE/DELETE)
- Procesando parámetros de auditoría `xd_`

## Instructions

### Step 1: Construir el query con `text()`

Usar `sqlalchemy.text()` con parámetros nombrados. El esquema `[dbo]` es obligatorio.

```python
from sqlalchemy import text, CursorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

query = text(
    """EXECUTE [dbo].[sp_setFormData]
        @userLogin = :user_login,
        @formId = :form_id,
        @valueText = :value_text
    """
)
params = {"user_login": user_login, "form_id": form_id, "value_text": value_text}
```

### Step 2: Ejecutar según tipo de operación

**Lectura (SELECT):** usar `async with self._session as session`.

```python
async with self._session as session:
    results = await session.execute(query, params)
```

**Escritura (INSERT/UPDATE/DELETE):** usar `try/except` con `commit()` y `rollback()`.

```python
try:
    results = await self._session.execute(query, params)
    await self._session.commit()
except SQLAlchemyError:
    await self._session.rollback()
    raise
```

### Step 3: Leer resultados defensivamente

Siempre verificar `CursorResult` y `returns_rows` antes de acceder a las filas.

**Múltiples filas:**
```python
if isinstance(results, CursorResult) and results.returns_rows:
    return [dict(zip(results.keys(), row)) for row in results.fetchall()]
return None
```

**Fila única:**
```python
if isinstance(results, CursorResult) and results.returns_rows:
    row = results.fetchone()
    return dict(zip(results.keys(), row)) if row else None
return None
```

### Step 4: Mapear parámetros xd_

| SQL Server (`camelCase`) | Python (`snake_case`) | Propósito |
|---|---|---|
| `@userLogin` | `user_login` | Usuario que ejecuta |
| `@formCode` | `form_code` | Código del formulario |
| `@periodCode` | `period_code` | Código del periodo |
| `@xd_creationUser` | `creation_user` | Usuario de creación |
| `@xd_lastUpdateUsr` | `update_user` | Último en modificar |

## Examples

- **Scenario**: Necesitas obtener el historial de un formulario desde un SP.
- **Action**: Crear un método en `FormRepository` que use `text("EXECUTE [dbo].[sp_getFormHistory] @formId = :form_id")`, ejecutar con `async with session`, y retornar `list[dict] | None`.

- **Scenario**: Necesitas guardar datos de celdas de un formulario.
- **Action**: Crear un método en `FormRepository` que use `text("EXECUTE [dbo].[sp_setFormData] ...")`, envolver en `try/except SQLAlchemyError` con `commit()` y `rollback()`.

## Troubleshooting

- **Problem**: SP retorna vacío pero hay datos en la DB.
- **Solution**: Verificar que las keys del dict `params` coincidan exactamente con los `:bind_names` en el query.

- **Problem**: `TypeError` al hacer `fetchall()`.
- **Solution**: Verificar `isinstance(results, CursorResult) and results.returns_rows` antes de leer.

- **Problem**: Los datos no se persisten tras un SP de escritura.
- **Solution**: Confirmar que se llama `await session.commit()` después del `execute()`.

## Validation Checklist

- [ ] Query usa esquema `[dbo].[sp_name]`
- [ ] Parámetros bindeados con `:param` (sin f-strings ni concatenación)
- [ ] `commit()` + `rollback()` en SPs de escritura
- [ ] `CursorResult` verificado antes de `fetchall()`/`fetchone()`
- [ ] Docstring menciona el nombre del SP
- [ ] Llamada vive en `repositories.py` (no en service ni endpoint)
