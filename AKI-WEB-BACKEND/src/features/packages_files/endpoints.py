from fastapi import APIRouter, Depends

from src.features.auth.dependencies import get_current_active_user
from src.features.auth.schemas import User
from .dependencies import get_packages_file_service
from .schemas import PackageFile
from .services import PackageFileService

router = APIRouter()


@router.get("/{package_id}/files", response_model=list[PackageFile])
async def list_package_files(package_id: str | int,
                             current_user: User = Depends(get_current_active_user),
                             packages_file_service: PackageFileService = Depends(get_packages_file_service)):
    return await packages_file_service.list_package_files(package_id=package_id)
