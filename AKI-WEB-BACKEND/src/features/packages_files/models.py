from sqlalchemy import Column, Integer, String, DateTime

from src.core import Base


class BulkUpload(Base):
    __tablename__ = 'bulk_uploads'

    bulk_id = Column("bulkId", Integer, primary_key=True)
    upload_id = Column("uploadId", Integer, primary_key=True)
    bulk_code = Column("bulkCode", String(100))
    upload_storage_Url = Column("uploadStorageUrl", String(1024))
    status = Column("status", String(1), nullable=False)
    xd_creation = Column("xd_creation", DateTime, nullable=False)
    xd_creation_user = Column("xd_creationUser", String(100), nullable=False)
    xd_last_update = Column("xd_lastUpdate", DateTime, nullable=False)
    xd_last_update_user = Column("xd_lastUpdateUsr", String(100), nullable=False)
