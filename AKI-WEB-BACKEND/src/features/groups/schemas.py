from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class Group(BaseModel):
    id: UUID = Field(..., alias="id")
    title: str = Field(..., alias="title")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)



class Period(BaseModel):
    id: UUID = Field(..., alias="id")
    title: str = Field(..., alias="title")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

