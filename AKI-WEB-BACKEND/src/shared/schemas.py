from typing import Any, Sequence

from pydantic import BaseModel, ConfigDict, Field


class ListItem(BaseModel):
    id: str | int
    title: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TreeNode(BaseModel):
    key: str | None = Field(None, alias="key")
    title: str | None = Field(None, alias="title")
    data: Any | None = Field(None, alias="data")
    icon: str | None = Field(None, alias="iconNot")
    is_leaf: bool | None = Field(None, alias="isLeaf")
    checked: bool | None = Field(False, alias="checked")
    selected: bool | None = Field(False, alias="selected")
    selectable: bool | None = Field(False, alias="selectable")
    disabled: bool | None = Field(None, alias="disabled")
    disable_checkbox: bool | None = Field(None, alias="disableCheckbox")
    expanded: bool | None = Field(None, alias="expanded")
    expanded_icon: str | None = Field(None, alias="expandedIcon")
    collapsed_icon: str | None = Field(None, alias="collapsedIcon")
    children: Sequence[Any] | None = Field(None, alias="children")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, extra='allow')
