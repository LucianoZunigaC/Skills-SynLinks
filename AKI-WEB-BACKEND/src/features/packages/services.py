import random
from datetime import UTC, datetime, timedelta
from io import BytesIO
from uuid import uuid4

import pandas as pd
from faker import Faker

from src.features.forms.repositories import FormRepository
from src.shared.services.blob_service import BlobService
from . import schemas, models
from .mappings import map_package_config_to_mapping, map_packages_to_tree
from .repositories import UploadRepository, PackageRepository, PeriodRepository
from .schemas import PackageDTO, PackageConfigDTO, UploadBase, ExcelFile, Worksheet
from .validators import validate_file_extension, validate_mime_type
from ...shared.schemas import TreeNode


class PackageService:
    def __init__(self, package_repository: PackageRepository, period_repository: PeriodRepository,
                 form_repository: FormRepository):
        self.fake = Faker()
        self.package_repository = package_repository
        self.period_repository = period_repository
        self.form_repository = form_repository

    async def get_packages_by_user_id(self, user_id: str, language_id: int | None = None) -> list[PackageDTO]:
        entities = await self.package_repository.get_packages_by_user_id(user_id=user_id, language_id=language_id)

        return [PackageDTO.model_validate(entity) for entity in entities]

    async def get_packages_in_tree(self, user_id: str, language_id: int | None = None) -> list[TreeNode]:
        entities = await self.get_packages_by_user_id(user_id=user_id, language_id=language_id)

        return map_packages_to_tree(entities)

    async def get_package_config_by_id(self, package_id: str | int, user_id: str, language_id: int | None = None) -> \
            list[PackageConfigDTO]:
        entities = await self.package_repository.get_package_config_by_id(bulk_id=package_id, user_id=user_id,
                                                                          language_id=language_id)

        return [PackageConfigDTO.model_validate(entity) for entity in entities]

    async def get_packages_mapping_by_id(self, package_id: str | int, user_id: str, language_id: int | None = None):
        entities = await self.get_package_config_by_id(package_id=package_id, user_id=user_id, language_id=language_id)

        mappings = []
        for entity in entities:
            next_period = await self.form_repository.get_next_period_by_id(form_id=entity.form_id)
            package_mapping = map_package_config_to_mapping(entity, next_period)
            mappings.append(package_mapping)
        return mappings

    def generate_periods(self):
        random_date = self.fake.date_between(start_date="-12M", end_date="today")
        last_period_loaded = random_date.strftime("%Y-%m")
        next_month = (datetime.strptime(last_period_loaded, "%Y-%m") + timedelta(days=32)).replace(day=1)
        next_period_to_load = next_month.strftime("%Y-%m")
        return last_period_loaded, next_period_to_load

    @staticmethod
    def generate_random_range():
        start_col = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        end_col = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        start_row = random.randint(1, 10)
        end_row = random.randint(11, 30)
        return f"{start_col}{start_row}:{end_col}{end_row}"

    async def form_includes_in_package(self, package_id: str | int, form_id: str | int, user_id: str, language_id: int | None = None):
        configs = await self.package_repository.get_package_config_by_id(bulk_id=package_id, user_id=user_id, language_id=language_id)
        return any(str(config['formId']).lower() == str(form_id).lower() for config in configs)


class UploadService:
    def __init__(self, upload_repository: UploadRepository, blob_service: BlobService):
        self.upload_repository = upload_repository
        self.blob_service = blob_service

    async def create_upload(self, upload: schemas.UploadBase) -> schemas.Upload | None:
        upload_data = models.Upload(file_name=upload.file_name,
                                    file_size=upload.file_size,
                                    file_content_type=upload.file_content_type,
                                    storage_url=upload.storage_url,
                                    xd_creation=upload.xd_creation,
                                    xd_creation_user=upload.xd_creation_user,
                                    xd_last_update=upload.xd_last_update,
                                    xd_last_update_user=upload.xd_last_update_user)
        entity = await self.upload_repository.create_upload(upload_data)
        return schemas.Upload.model_validate(entity) if entity else None

    async def get_upload(self, upload_id: str | int) -> schemas.Upload | None:
        entity = await self.upload_repository.get(upload_id=upload_id)

        return schemas.Upload.model_validate(entity) if entity else None

    async def process_excel_upload(self, package_id: str | int, file_name: str, file_content_type: str,
                                   file_content: bytes, user_id: str):
        self.validate_file_name(file_name, file_content_type)

        storage_url = await self.blob_service.upload_file(str(uuid4()), BytesIO(file_content))

        create_upload = UploadBase(file_name=file_name,
                                   file_size=len(file_content),
                                   file_content_type=file_content_type,
                                   storage_url=storage_url,
                                   xd_creation=datetime.now(UTC),
                                   xd_creation_user=user_id,
                                   xd_last_update=datetime.now(UTC),
                                   xd_last_update_user=user_id)
        upload = await self.create_upload(create_upload)

        with pd.ExcelFile(file_content) as xls:
            worksheet_details = [Worksheet(max_column=worksheet.max_column,
                                           max_row=worksheet.max_row,
                                           min_column=worksheet.min_column,
                                           min_row=worksheet.min_row,
                                           sheet_state=worksheet.sheet_state,
                                           title=worksheet.title
                                           )
                                 for worksheet in xls.book.worksheets
                                 ]

            return ExcelFile(
                id=upload.id,
                filename=file_name,
                size=len(file_content),
                content_type=file_content_type,
                worksheets=worksheet_details
            )

    def validate_file_name(self, file_name: str, file_content_type: str | None = None):
        # Validar la extensión del archivo
        file_extension = "." + file_name.split(".")[-1].lower()

        # Validar la extensión del archivo
        validate_file_extension(file_extension)

        # Validar el tipo MIME del archivo
        validate_mime_type(file_content_type)


class PeriodService:
    def __init__(self, repository: PeriodRepository):
        self.repository = repository

    async def get_period(self, period_id: str | int) -> schemas.PeriodInDB | None:
        entity = await self.repository.get(period_id=period_id)

        return schemas.PeriodInDB.model_validate(entity) if entity else None

    async def get_next_period(self, period_id: str | int) -> schemas.PeriodInDB | None:
        entity = await self.repository.get_next_period(period_id=period_id)

        return schemas.PeriodInDB.model_validate(entity) if entity else None
