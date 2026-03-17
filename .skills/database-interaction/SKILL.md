---
name: database-interaction
description: "This skill should be used when configuring session_manager, implementing the Repository pattern with BaseRepository, writing SQLAlchemy 2.0 async queries, and managing transactions in aki-web-backend."
metadata:
  author: aki-team
  version: 1.0.0
risk: safe
---

# Database Interaction — aki-web-backend

## Purpose

Standard para la capa de persistencia del proyecto. Toda lógica de acceso a datos debe vivir en `repositories.py` y usar `session_manager` de `src.core`.

## When to Use This Skill

This skill should be used when:
- Configurando el `session_manager`
- Implementando el patrón Repository (heredando de `BaseRepository`)
- Escribiendo consultas asíncronas de SQLAlchemy 2.0 (`select()`)
- Manejando transacciones de escritura (commit, refresh, rollback)

## Instructions

### Step 1: Configurar el lifespan en `main.py`

La inicialización y cierre de la DB se maneja en el lifespan de FastAPI.

```python
# src/main.py
from src.core import session_manager
from src.config import settings

@asynccontextmanager
async def lifespan(_: FastAPI):
    session_manager.init(
        settings.sqlalchemy_database_uri,
        sqlalchemy_echo=settings.sqlalchemy_echo,
    )
    yield
    await session_manager.close(raise_exception=False)
```

### Step 2: Crear el repositorio heredando BaseRepository

Cada feature tiene su repositorio en `src/features/{feature}/repositories.py`.
Heredar de `BaseRepository[Entity, ID]` definido en `src/shared/base_repository.py`.

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.base_repository import BaseRepository
from .models import Form

class FormRepository(BaseRepository[Form, int]):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, entity_id: int) -> Form | None:
        stmt = select(Form).filter(Form.id == entity_id)
        result = await self._session.execute(stmt)
        return result.scalars().first()
```

### Step 3: Usar select() de SQLAlchemy 2.0

Usar **siempre** `select()` asíncrono. Prohibido `session.query()` (legacy, bloquea el event loop).

```python
# Filtros dinámicos
async def list_active(self) -> list[Form]:
    stmt = (
        select(Form)
        .filter(Form.status == 'A')
        .order_by(Form.xd_creation)
    )
    result = await self._session.execute(stmt)
    return list(result.scalars().all())
```

### Step 4: Manejar transacciones de escritura

Siempre hacer `commit()` + `refresh()` en creaciones, y `rollback()` en excepciones.

```python
async def create(self, entity: Form) -> Form:
    try:
        self._session.add(entity)
        await self._session.commit()
        await self._session.refresh(entity)
        return entity
    except Exception:
        await self._session.rollback()
        raise
```

### Step 5: Inyectar la sesión vía dependencia

Usar `AsyncSessionDep` de `src.core.dependencies` en endpoints.

```python
# src/features/{feature}/dependencies.py
from src.core import AsyncSessionDep

async def get_form_repository(session: AsyncSessionDep):
    yield FormRepository(session)
```

## Examples

- **Scenario**: Crear un repositorio para una nueva feature "groups".
- **Action**: Crear `src/features/groups/repositories.py`, definir `GroupRepository(BaseRepository[Group, int])`, inyectar `AsyncSession` en `__init__`, implementar `get()`, `list()`, `create()`.

- **Scenario**: Necesitas filtrar entidades por múltiples campos opcionales.
- **Action**: Construir una lista `filters = []`, agregar condiciones con `.append()`, y pasar `*filters` a `select(Model).filter(*filters)`.

## Troubleshooting

- **Problem**: `MissingGreenlet` error en consultas.
- **Solution**: Todas las operaciones SQLAlchemy async deben estar en funciones `async def` con `await`.

- **Problem**: Entidad no tiene ID tras `add()`.
- **Solution**: Llamar `await session.refresh(entity)` después del `commit()`.

- **Problem**: `session.query()` bloquea la aplicación.
- **Solution**: Reemplazar con `select()` + `await session.execute(stmt)`.

## Validation Checklist

- [ ] Lifespan usa `session_manager.init()` y `session_manager.close()`
- [ ] Repositorio hereda de `BaseRepository[Entity, ID]`
- [ ] Queries usan `select()` (no `session.query()`)
- [ ] Escrituras hacen `commit()` → `refresh()` → `rollback()` en except
- [ ] Listas ordenadas por `xd_creation`
- [ ] Sesión inyectada via `AsyncSessionDep`
