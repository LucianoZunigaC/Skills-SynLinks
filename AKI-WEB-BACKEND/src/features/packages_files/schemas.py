import uuid
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class BulkUploadDTO(BaseModel):
    bulk_id: int = Field(..., alias="bulkId")
    upload_id: int = Field(..., alias="uploadId")
    bulk_code: str = Field(..., alias="bulkCode")
    upload_storage_Url: str = Field(..., alias="uploadStorageUrl")
    status: str = Field(..., alias="status")
    xd_creation: datetime = Field(..., alias="xd_creation")
    xd_creation_user: str = Field(..., alias="xd_creationUser")
    xd_last_update: datetime = Field(..., alias="xd_lastUpdate")
    xd_last_update_user: str = Field(..., alias="xd_lastUpdateUsr")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PackageFile(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    package_id: str = Field(..., alias="packageId")
    file_name: str = Field(..., alias="fileName")
    file_size: int = Field(..., alias="fileSize")
    file_type: str = Field(..., alias="fileType")
    upload_date: datetime = Field(..., alias="uploadDate")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
