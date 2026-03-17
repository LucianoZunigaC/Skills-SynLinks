import contextlib
import logging
from typing import AsyncIterator, Any

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine, AsyncConnection, AsyncSession

try:
    from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
except ImportError:
    SQLAlchemyInstrumentor = None
from .base import Base


class DatabaseSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._session_maker: async_sessionmaker | None = None
        self._logger = logging.getLogger(__name__)

    def init(self,
             url: str | URL,
             sqlalchemy_echo: bool = False,
             otel_enable_commenter: bool = False,
             otel_enable_attribute_commenter: bool = False,
             otel_commenter_options: dict[str, Any] | None = None):
        self._engine = create_async_engine(url, echo=sqlalchemy_echo)
        # Instrument SQLAlchemy with OpenTelemetry on the underlying sync engine
        if SQLAlchemyInstrumentor is not None:
            try:
                SQLAlchemyInstrumentor().instrument(engine=self._engine.sync_engine,
                                                    enable_commenter=otel_enable_commenter,
                                                    enable_attribute_commenter=otel_enable_attribute_commenter,
                                                    commenter_options=otel_commenter_options)
            except Exception as e:
                self._logger.debug(f"Failed to instrument SQLAlchemy: {e}")
        else:
            self._logger.debug("opentelemetry-instrumentation-sqlalchemy not installed; skipping instrumentation.")
        self._session_maker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self, raise_exception: bool = True):
        if self._engine is None:
            if raise_exception:
                raise Exception("DatabaseSessionManager is not initialized")
            return
        # Safely uninstrument the engine to avoid duplicate instrumentation on re-init
        if SQLAlchemyInstrumentor is not None:
            try:
                SQLAlchemyInstrumentor().uninstrument(engine=self._engine.sync_engine)
            except Exception:
                pass
        await self._engine.dispose()
        self._engine = None
        self._session_maker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._session_maker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._session_maker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    # Used for testing
    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)
