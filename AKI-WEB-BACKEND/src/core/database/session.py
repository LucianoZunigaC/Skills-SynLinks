from .session_manager import DatabaseSessionManager

session_manager = DatabaseSessionManager()

async def get_async_session():
    async with session_manager.session() as session:
        yield session


async def get_async_connection():
    async with session_manager.connect() as connection:
        yield connection 