from fastapi import Depends

from src.features.forms.dependencies import get_form_repository
from src.features.forms.repositories import FormRepository
from .repositories import UploadRepository, PackageRepository, PeriodRepository
from .services import PackageService, UploadService, PeriodService
from ...core import AsyncSessionDep
from ...shared.dependencies import get_blob_service
from ...shared.services.blob_service import BlobService


async def get_period_repository(db: AsyncSessionDep):
    yield PeriodRepository(db)


async def get_period_service(period_repository: PeriodRepository = Depends(get_period_repository)):
    yield PeriodService(period_repository)


async def get_package_repository(session: AsyncSessionDep):
    yield PackageRepository(session)


async def get_package_service(package_repository: PackageRepository = Depends(get_package_repository),
                              period_repository: PeriodRepository = Depends(get_period_repository),
                              form_repository: FormRepository = Depends(get_form_repository)):
    yield PackageService(package_repository, period_repository, form_repository)


async def get_upload_repository(db: AsyncSessionDep):
    yield UploadRepository(db)


async def get_upload_service(upload_repository: UploadRepository = Depends(get_upload_repository),
                             blob_service: BlobService = Depends(get_blob_service)):
    yield UploadService(upload_repository, blob_service)
