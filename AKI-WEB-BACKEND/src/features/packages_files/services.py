from .repositories import BulkUploadRepository
from .schemas import BulkUploadDTO


class PackageFileService:
    def __init__(self, bulk_upload_repository: BulkUploadRepository | None = None):
        self.bulk_upload_repository = bulk_upload_repository

    async def list_package_files(self, package_id: str | int):
        entities = await self.bulk_upload_repository.get_bulk_uploads_by_id(bulk_id=package_id)
        return [BulkUploadDTO.model_validate(entity) for entity in entities]
