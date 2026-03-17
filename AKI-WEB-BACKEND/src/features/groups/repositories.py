from sqlalchemy.ext.asyncio import AsyncSession


class GroupRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    def __init__(self):
        self.sample = ''
