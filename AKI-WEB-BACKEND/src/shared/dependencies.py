from fastapi import Depends

from src.config import settings
from src.shared.repositories.blob_repository import BlobRepository
from src.shared.services.blob_service import BlobService


async def get_blob_repository():
    yield BlobRepository(settings.AZURE_STORAGE_CONNECTION_STRING, settings.PACKAGE_UPLOADS_CONTAINER_NAME)


async def get_blob_service(repository=Depends(get_blob_repository)):
    yield BlobService(repository)
