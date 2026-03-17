import json
from datetime import datetime, UTC
from enum import Enum, StrEnum
from typing import Sequence, Any
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, field_validator


class PackageDTO(BaseModel):
    group_id: str | int | None = Field(None, alias="groupId")
    group_name: str | None = Field(None, alias="groupName")
    bulk_id: str | int | None = Field(None, alias="bulkId")
    bulk_code: str | None = Field(None, alias="bulCode")
    short_name: str | None = Field(None, alias="shortName")
    full_name: str | None = Field(None, alias="fullName")
    description: str | None = Field(None, alias="description")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PackageImportConfig(BaseModel):
    use_columns: str | None = Field(None, alias="useColumns")
    header_row: int | list[int] = Field(0, alias="headerRow")
    sheet_name: str | None = Field(None, alias="sheetName")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PackageConfigDTO(BaseModel):
    bulk_id: str | int | None = Field(None, alias="bulkId")
    bulk_code: str | None = Field(None, alias="bulkCode")
    form_id: str | int | None = Field(None, alias="formId")
    form_code: str | None = Field(None, alias="formCode")
    form_type_code: str | None = Field(None, alias="formTypeCode")
    short_name: str | None = Field(None, alias="shortName")
    granularity: str = Field(..., alias="granularity")
    layout: str = Field(..., alias="layout")
    trasposed: bool = Field(..., alias="transposed")
    has_form_access: str | None = Field(None, alias="hasFormAccess")
    import_query: PackageImportConfig | None = Field(None, alias="importQuery")
    period_id: int = Field(..., alias="periodId")
    period_code: str = Field(..., alias="periodCode")
    period_label: str = Field(..., alias="perLabel")

    @field_validator('import_query', mode='before')
    @classmethod
    def validate_import_query(cls, v: Any) -> PackageImportConfig | None:
        if v is None:
            return None
        try:
            obj = json.loads(v)
            return PackageImportConfig.model_validate(obj)
        except Exception:
            return None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PackageMapping(BaseModel):
    bulk_id: UUID | str | int = Field(..., alias="packageId")
    bulk_code: str | None = Field(None, alias="packageCode")
    form_id: UUID | str | int = Field(..., alias="formId")
    form_code: str | None = Field(None, alias="formCode")
    form_name: str = Field(..., alias="formName")
    sheet_name: str = Field(..., alias="sheetName")
    range: str | None = Field(None, alias="range")
    period_id: UUID | str | int = Field(..., alias="periodId")
    period_code: str = Field(..., alias="periodCode")
    last_period: str = Field(..., alias="lastPeriod")
    next_period: str = Field(..., alias="nextPeriod")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class Package(BaseModel):
    id: UUID = Field(..., alias="id")
    title: str = Field(..., alias="title")
    forms: Sequence[Any] = Field(..., alias="forms")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)



class SheetState(str, Enum):
    VERY_HIDDEN = 'veryHidden'
    HIDDEN = 'hidden'
    VISIBLE = 'visible'


class Worksheet(BaseModel):
    max_column: int = Field(..., alias="maxColumn",
                            description="The highest column index containing data (1-based index, e.g., 1 for column A).")
    max_row: int = Field(..., alias="maxRow",
                         description="The highest row index containing data (1-based index, e.g., 1 for the first row).")
    min_column: int = Field(..., alias="minColumn",
                            description="The lowest column index containing data (1-based index, e.g., 1 for column A).")
    min_row: int = Field(..., alias="minRow",
                         description="The lowest row index containing data (1-based index, e.g., 1 for the first row).")
    sheet_state: SheetState = Field(SheetState.VISIBLE, alias="sheetState",
                                    description="The visibility state of the sheet. Possible values: ‘veryHidden’, ‘hidden’, or ‘visible’.")
    title: str = Field(..., alias="title", description="The title or name of the worksheet.")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ExcelFile(BaseModel):
    id: UUID | str | int = Field(..., alias="id", description="Unique identifier for the Excel file.")
    filename: str | None = Field(None, alias="filename",
                                 description="The name of the Excel file, including its extension (e.g., 'file.xlsx').")
    size: int | None = Field(None, alias="size", description="The size of the Excel file in bytes.")
    content_type: str | None = Field(None, alias="contentType",
                                     description="The MIME type of the Excel file (e.g., 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet').")
    worksheets: Sequence[Worksheet] = Field(..., alias="worksheets",
                                            description="A list of worksheets contained in the Excel file.")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class UploadBase(BaseModel):
    file_name: str | None = Field(None, max_length=255, alias="fileName")
    file_size: int | None = Field(None, gt=0, alias="fileSize")
    file_content_type: str | None = Field(None, max_length=100, alias="fileContentType")
    storage_url: str | None = Field(None, max_length=1024, alias="storageUrl")
    xd_creation: datetime = Field(datetime.now(UTC), alias="created", exclude=True)
    xd_creation_user: str = Field(..., alias="authorId", exclude=True)
    xd_last_update: datetime = Field(datetime.now(UTC), alias="modified", exclude=True)
    xd_last_update_user: str = Field(..., alias="editorId", exclude=True)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class Upload(UploadBase):
    id: str | int = Field(None, alias="id")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PackageFormAction(StrEnum):
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'



class UpdatePackageMapping(BaseModel):
    file_id: str | int | None = Field(None, alias="fileId")
    sheet_name: str | int | None = Field(None, alias="sheetName")
    action: PackageFormAction | None = Field(None, alias="action")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ValidatePackageMapping(BaseModel):
    file_id: str | int | None = Field(None, alias="fileId")
    sheet_name: str | int | None = Field(None, alias="sheetName")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PackageMappingValidate(BaseModel):
    bulk_id: UUID | str | int = Field(..., alias="packageId")
    form_id: UUID | str | int = Field(..., alias="formId")
    file_id: str | int | None = Field(None, alias="fileId")
    sheet_name: str | int | None = Field(None, alias="sheetName")
    status: str | None = Field(None, alias="status")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PeriodBase(BaseModel):
    calendar_code: str = Field(..., alias="calendarCode")
    type: str = Field(..., alias="type")
    sub_type: str | None = Field(None, alias="subType")
    code: str = Field(..., alias="code")
    p_year: int | None  = Field(None, alias="periodYear")
    p_month: int | None = Field(None, alias="periodMonth")
    p_start: datetime = Field(..., alias="periodStart")
    p_end: datetime = Field(..., alias="periodEnd")
    label1: str = Field(..., alias="label1")
    label2: str | None  = Field(None, alias="label2")
    label3: str | None  = Field(None, alias='label3')
    entity_type: str = Field(..., alias="fileName")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class PeriodInDB(PeriodBase):
    id: str | int = Field(..., alias="created")
    xd_creation: datetime = Field(..., alias="created", exclude=True)
    xd_creation_user: str = Field(..., alias="authorId", exclude=True)
    xd_last_update: datetime = Field(..., alias="modified", exclude=True)
    xd_last_update_user: str = Field(..., alias="editorId", exclude=True)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
