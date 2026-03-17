from pydantic import BaseModel, Field, ConfigDict


class UserCreate(BaseModel):
    username: str = Field(..., alias="username")
    email: str = Field(..., alias="email")
    name: str = Field(..., alias="name")
    last_name: str = Field(..., alias="lastName")
    password: str = Field(..., alias="password")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
