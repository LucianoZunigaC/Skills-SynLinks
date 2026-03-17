from fastapi import Depends

from .repositories import BulkUploadRepository
from .services import PackageFileService
from ...core import AsyncSessionDep


async def get_bulk_upload_repository(db: AsyncSessionDep):
    yield BulkUploadRepository(db)


async def get_packages_file_service(bulk_upload_repository: BulkUploadRepository = Depends(get_bulk_upload_repository)):
    yield PackageFileService(bulk_upload_repository=bulk_upload_repository)
