from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import BulkUpload


class BulkUploadRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_bulk_uploads_by_id(self, bulk_id: str | int):
        filters = []
        if bulk_id:
            filters.append(BulkUpload.bulk_id == bulk_id)

        stmt = select(BulkUpload).filter(*filters).order_by(BulkUpload.xd_creation)
        result = await self._session.execute(stmt)
        return result.scalars().all()
