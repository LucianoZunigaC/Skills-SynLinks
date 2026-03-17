from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection

from .database import get_async_session, get_async_connection

# Common dependency types for database access

# AsyncSessionDep provides type-safe database session dependency
AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]

# AsyncConnectionDep provides type-safe database connection dependency 
AsyncConnectionDep = Annotated[AsyncConnection, Depends(get_async_connection)]
