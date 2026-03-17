from typing import List

from sqlalchemy import text, CursorResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.packages.models import Upload, Period


class PackageRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_packages_by_user_id(self, user_id: str, language_id: int | None = None) -> List[dict] | None:
        """
        Get packages summary by user ID.

        Args:
            user_id (str): The ID of the user.
            language_id (int, optional): The language ID.

        Returns:
            List of dictionaries containing the packages summary.
        """
        query = text('''EXECUTE [dbo].[sp_getBulkPackList] 
                        @userLogin = :user_id,
                        @languageId = :language_id
                    ''')
        params = {'user_id': user_id, 'language_id': language_id}
        async with self._session as session:
            results = await session.execute(query, params)

            if isinstance(results, CursorResult) and results.returns_rows:
                rows = results.fetchall()
                keys = results.keys()

                return [dict(zip(keys, row)) for row in rows]
            return None

    async def get_package_config_by_id(self, bulk_id, user_id, language_id) -> List[dict] | None:
        query = text('''EXECUTE [dbo].[sp_getBulkPackCfg] 
                        @bulkId = :bulk_id,
                        @userLogin = :user_id,
                        @languageId = :language_id
                    ''')
        params = {'bulk_id': bulk_id, 'user_id': user_id, 'language_id': language_id}

        async with self._session as session:
            results = await session.execute(query, params)

            if isinstance(results, CursorResult) and results.returns_rows:
                rows = results.fetchall()
                keys = results.keys()

                return [dict(zip(keys, row)) for row in rows]
            return None


class UploadRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_upload(self, entity: Upload) -> Upload:
        self._session.add(entity)
        await self._session.commit()
        await self._session.refresh(entity)
        return entity

    async def get(self, upload_id):
        filters = []
        if upload_id:
            filters.append(Upload.id == upload_id)

        stmt = select(Upload).filter(*filters).order_by(Upload.xd_creation)
        result = await self._session.execute(stmt)
        return result.scalars().first()


class PeriodRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self, period_id):
        filters = []
        if period_id:
            filters.append(Period.id == period_id)

        stmt = select(Period).filter(*filters).order_by(Period.xd_creation)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_next_period(self, period_id):
        current = await self.get(period_id=period_id)

        filters = [Period.calendar_code == current.calendar_code,
                   Period.type == current.type,
                   Period.sub_type == current.sub_type,
                   Period.p_start > current.p_start]

        stmt = select(Period).filter(*filters).order_by(Period.xd_creation)
        result = await self._session.execute(stmt)
        return result.scalars().first()