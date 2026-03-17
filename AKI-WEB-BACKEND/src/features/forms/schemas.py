from datetime import datetime
from typing import List, Sequence, Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, field_validator, AliasChoices

from src.shared.utils import field_validator_generic


class Form(BaseModel):
    id: UUID = Field(..., alias="id")
    title: str = Field(..., alias="title")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PaginationParams(BaseModel):
    limit: int | None = Field(500, gt=0)
    offset: int | None = Field(0, ge=0)


class FilterParams(BaseModel):
    filter: str | None = Field(None)


class SortParams(BaseModel):
    sort: str | None = Field(None)


class SelectParams(BaseModel):
    select: List[str] | None = Field(None)


class ExpandParams(BaseModel):
    expand: List[str] | None = Field(None)


class FormPeriodBase(BaseModel):
    id: int = Field(..., alias="id")
    form_id: int = Field(..., alias="formId")
    period_id: int = Field(..., alias="periodId")
    form_code: str = Field(..., alias="formCode")
    period_code: str = Field(..., alias="periodCode")
    status: str = Field(..., alias="status", exclude=True)
    xd_creation: datetime = Field(..., alias="created", exclude=True)
    xd_creation_user: str = Field(..., alias="authorId", exclude=True)
    xd_last_update: datetime = Field(..., alias="modified", exclude=True)
    xd_last_update_user: str = Field(..., alias="editorId", exclude=True)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class FormBase(BaseModel):
    id: int = Field(..., alias="id")
    code: str = Field(..., alias="code")
    form_type_id: int = Field(..., alias="formTypeId")
    template_id: int = Field(..., alias="templateId")
    short_name: str = Field(..., alias="shortName")
    full_name: str = Field(..., alias="fullName")
    description: str = Field(..., alias="description")
    layout: str = Field(..., alias="layout")
    trasposed: bool = Field(..., alias="transposed")
    granularity: str = Field(..., alias="granularity")
    form_type_code: str = Field(..., alias="formTypeCode")
    template_code: str = Field(..., alias="templateCode")
    status: str = Field(..., alias="status", exclude=True)
    entity_type: str = Field(..., alias="entityType")
    xd_creation: datetime = Field(..., alias="created", exclude=True)
    xd_creation_user: str = Field(..., alias="authorId", exclude=True)
    xd_last_update: datetime = Field(..., alias="modified", exclude=True)
    xd_last_update_user: str = Field(..., alias="editorId", exclude=True)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class FormAbstractColumnDefinition(BaseModel):
    header_name: str | None = Field(None, alias="headerName")
    header_tooltip: str | None = Field(None, alias="headerTooltip")
    suppress_columns_tool_panel: bool | None = Field(None, alias="suppressColumnsToolPanel")
    suppress_filters_tool_panel: bool | None = Field(None, alias="suppressFiltersToolPanel")
    pivot_keys: Sequence[str] | None = Field(None, alias="pivotKeys")
    cell_aria_role: str | None = Field(None, alias="cellAriaRole")
    wrap_header_text: bool | None = Field(None, alias="wrapHeaderText")
    auto_header_height: bool | None = Field(None, alias="autoHeaderHeight")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class FormColumnDefinition(FormAbstractColumnDefinition):
    col_id: str | None = Field(None, alias="colId")
    field: str | None = Field(None, alias="field")
    cell_editor: str | Sequence[str] | None = Field(None, alias="cellEditor")
    hide: bool | None = Field(None, alias="hide")
    editable: bool | None = Field(None, alias="editable")
    flex: int | None = Field(None, alias="flex")
    initial_width: int | None = Field(None, alias="initialWidth")
    width: int | None = Field(None, alias="width")
    single_click_edit: bool | None = Field(None, alias="singleClickEdit")
    filter: str | None = Field(None, alias="filter")
    cell_class: str | None = Field(None, alias="cellClass")
    pinned: str | None = Field(None, alias="pinned")
    suppress_movable: bool | None = Field(None, alias="suppressMovable")
    resizable: bool | None = Field(None, alias="resizable")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class FormColumnGroupDefinition(FormAbstractColumnDefinition):
    children: list[Any] | list[FormColumnDefinition] | None = Field(None, alias="children")
    group_id: str | None = Field(None, alias="groupId")
    open_by_default: bool | None = Field(None, alias="openByDefault")
    marry_children: bool | None = Field(None, alias="marryChildren")
    suppress_sticky_label: bool | None = Field(None, alias="suppressStickyLabel")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class FormHistoryBase(BaseModel):
    form_id: int | None = Field(None, alias="formId", validation_alias="formId")
    short_name: str = Field(..., alias="shortName", validation_alias="shortName")
    period_id: int = Field(..., alias="periodId", validation_alias="periodId")
    period_type: str = Field(..., alias="periodType", validation_alias="periodType")
    period_code: str = Field(..., alias="periodCode", validation_alias="periodCode")
    period_label: str = Field(..., alias="periodLabel", validation_alias="periodLabel")
    period_start: datetime = Field(..., alias="periodStart", validation_alias="periodStart")
    period_end: datetime = Field(..., alias="periodEnd", validation_alias=AliasChoices("periodEnd", "pEnd"))

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class FormHistory(FormHistoryBase):
    period_status: bool | None = Field(None, alias="periodStatus", validation_alias="periodStatus")
    period_version: int = Field(..., alias="periodVersion", validation_alias="periodVersion")
    period_last_update: datetime = Field(..., alias="modified", validation_alias="periodLastUpdate")
    period_last_update_user: str = Field(..., alias="editorId", validation_alias="periodlastUpdateUsr")

    @field_validator('period_status', mode='before')
    @classmethod
    def field_validator_status(cls, v: Any):
        return field_validator_generic(v, true_values='a', false_values='i')

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class FormDataBase(BaseModel):
    form_id: int | None = Field(None, alias="formId", validation_alias="formId")
    period_id: int | None = Field(None, alias="periodId", validation_alias="periodId")
    period_point: datetime = Field(False, alias="periodPoint", validation_alias="periodPoint")
    scenario_id: int | None = Field(None, alias="scenarioId", validation_alias="scenarioId")
    location_id: int | None = Field(None, alias="locationId", validation_alias="locationId")
    measure_id: int | None = Field(None, alias="measureId", validation_alias="measureId")

    value_int: int | None = Field(None, alias="valueInt", validation_alias="valueInt")
    value_dec: float | None = Field(None, alias="valueDec", validation_alias="valueDec")
    value_float: float | None = Field(None, alias="valueFloat", validation_alias="valueFloat")
    value_text: str | None = Field(None, alias="valueText", validation_alias="valueText")
    value_boolean: bool | None = Field(None, alias="valueBoolean", validation_alias="valueBoolean")
    value_datetime: datetime | None = Field(None, alias="valueDateTime", validation_alias="valueDateTime")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class FormData(FormDataBase):
    row_number: int | None = Field(None, alias="rowNumber", validation_alias="rowNumber")
    col_number: int | None = Field(None, alias="colNumber", validation_alias="colNumber")
    data_type_code: str | None = Field(None, alias="dataTypeCode", validation_alias="dataTypeCode")
    form_code: str | str | None = Field(None, alias="formCode", validation_alias="formCode")
    period_code: str | int | None = Field(None, alias="periodCode", validation_alias="periodCode")
    scenario_code: str | None = Field(None, alias="scenarioCode", validation_alias="scenarioCode")
    location_code: str | None = Field(None, alias="locationCode", validation_alias="locationCode")
    measure_code: str | None = Field(None, alias="measureCode", validation_alias="measureCode")
    is_filler: bool | None = Field(None, alias="isFiller", validation_alias="isFiller")
    can_edit: bool | None = Field(None, alias="canEdit", validation_alias="canEdit")
    label_01: str | None = Field(None, alias="label01", validation_alias="label01")
    label_02: str | None = Field(None, alias="label02", validation_alias="label02")
    values_table_row_id: int | None = Field(None, alias="valuesTableRowId", validation_alias="valuesTableRowId")

    @field_validator('is_filler', 'can_edit', mode='before')
    @classmethod
    def field_validator_bool(cls, v: Any):
        return field_validator_generic(v, true_values='y', false_values='n')

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CreateFormData(FormDataBase):
    user_id: str | None = Field(None, alias="userId")
    # form_id: str | None = Field(None, alias="formId", validation_alias="formId")
    # period_id: str | None = Field(None, alias="periodId", validation_alias="periodId")
    # period_point: date | None = Field(None, alias="periodPoint", validation_alias="periodPoint")
    # scenario_id: str | None = Field(None, alias="scenarioId", validation_alias="scenarioId")
    # location_id: str | None = Field(None, alias="locationId", validation_alias="locationId")
    # measure_id: str | None = Field(None, alias="measureId", validation_alias="measureId")
    form_code: str | None = Field(None, alias="formCode", validation_alias="formCode")
    period_code: str | int | None = Field(None, alias="periodCode", validation_alias="periodCode")
    scenario_code: str | None = Field(None, alias="scenarioCode", validation_alias="scenarioCode")
    location_code: str | None = Field(None, alias="locationCode", validation_alias="locationCode")
    measure_code: str | None = Field(None, alias="measureCode", validation_alias="measureCode")
    # value: Any | None = Field(None, alias="value", validation_alias="value")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class SceneryBase(BaseModel):
    id: int = Field(..., alias="id")
    code: str = Field(..., alias="code")
    short_name: str = Field(..., alias="shortName")
    full_name: str = Field(..., alias="fullName")
    description: str = Field(..., alias="description")
    status: str = Field(..., alias="status", exclude=True)
    entity_type: str = Field(..., alias="entityType")
    xd_creation: datetime = Field(..., alias="created", exclude=True)
    xd_creation_user: str = Field(..., alias="authorId", exclude=True)
    xd_last_update: datetime = Field(..., alias="modified", exclude=True)
    xd_last_update_user: str = Field(..., alias="editorId", exclude=True)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class LocationStructureBase(BaseModel):
    id: int = Field(..., alias="id")
    node_type_id: int = Field(..., alias="nodeTypeId")
    node_type_code: str = Field(..., alias="nodeTypeCode")
    node_code: str = Field(..., alias="nodeCode")
    short_name: str = Field(..., alias="shortName")
    full_name: str = Field(..., alias="fullName")
    description: str = Field(..., alias="description")
    parent_id: int = Field(..., alias="parentId")
    parent_code: str = Field(..., alias="parentCode")
    path: str = Field(..., alias="path")
    depth: int = Field(..., alias="depth")
    height: int = Field(..., alias="code")
    has_children: bool = Field(..., alias="hasChildren")
    status: str = Field(..., alias="status", exclude=True)
    entity_type: str = Field(..., alias="entityType")
    xd_creation: datetime = Field(..., alias="created", exclude=True)
    xd_creation_user: str = Field(..., alias="authorId", exclude=True)
    xd_last_update: datetime = Field(..., alias="modified", exclude=True)
    xd_last_update_user: str = Field(..., alias="editorId", exclude=True)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class MeasureBase(BaseModel):
    id: int = Field(..., alias="id")
    code: str = Field(..., alias="code")
    short_name: str = Field(..., alias="shortName")
    full_name: str = Field(..., alias="fullName")
    description: str = Field(..., alias="description")
    uom_id: int = Field(..., alias="uomId")
    data_type_code: str = Field(..., alias="dataTypeCode")
    status: str = Field(..., alias="status", exclude=True)
    entity_type: str = Field(..., alias="entityType")
    xd_creation: datetime = Field(..., alias="created", exclude=True)
    xd_creation_user: str = Field(..., alias="authorId", exclude=True)
    xd_last_update: datetime = Field(..., alias="modified", exclude=True)
    xd_last_update_user: str = Field(..., alias="editorId", exclude=True)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class UserFormsSummary(BaseModel):
    group_id: int | None = Field(None, alias="groupId")
    group_name: str | None = Field(None, alias="groupName")
    form_id: int = Field(..., alias="formId")
    short_name: str = Field(..., alias="shortName")
    form_type_code: str = Field(..., alias="formTypeCode")
    granularity: str = Field(..., alias="granularity")
    layout: str = Field(..., alias="layout")
    trasposed: bool = Field(..., alias="trasposed")
    period_code: str = Field(..., alias="periodCode")
    last_update: datetime = Field(..., alias="lastUpdate")
    period_version: int = Field(..., alias="periodVersion")
    period_label: str = Field(..., alias="periodLabel")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class FormNavigationMenu(BaseModel):
    id: int
    name: str
    isGroup: bool
    lastUpdate: Optional[datetime] = None
    periodVersion: Optional[int] = None
    periodLabel: Optional[str] = None
    children: Optional[list['FormNavigationMenu']] = []


class FormAddPeriod(BaseModel):
    user_id: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class FormRowDefinition(BaseModel):
    __pydantic_extra__: dict[str, Any] = Field(init=False)

    row_id: int | None = Field(None, alias="rowId", validation_alias=AliasChoices("rowId", "rowNumber"))
    form_id: int | None = Field(None, alias="formId")
    period_id: int | None = Field(None, alias="periodId")
    scenario_id: int | None = Field(None, alias="scenarioId")
    location_id: int | None = Field(None, alias="locationId")
    measure_id: int | None = Field(None, alias="measureId")
    form_code: str | None = Field(None, alias="formCode")
    period_code: str | None = Field(None, alias="periodCode")
    scenario_code: str | None = Field(None, alias="scenarioCode")
    location_code: str | None = Field(None, alias="locationCode")
    measure_code: str | None = Field(None, alias="measureCode")
    # cell_group: bool | None = Field(None, alias="cellGroup")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, extra='allow')


class FormEntry(BaseModel):
    id: UUID | str | int
    value: str | int | float | None = Field(None)
    col_def: FormColumnDefinition | None = Field(None, alias='colDef')
    row_def: FormRowDefinition | None = Field(None, alias='rowDef')

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
