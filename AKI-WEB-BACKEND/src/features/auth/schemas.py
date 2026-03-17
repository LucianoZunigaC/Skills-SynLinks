from typing import Any

from pydantic import BaseModel, Field, ConfigDict, computed_field, field_validator


class Token(BaseModel):
    access_token: str = Field(...)
    token_type: str = Field("Bearer")
    expires_in: float = Field(...)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TokenData(BaseModel):
    username: str | None = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class User(BaseModel):
    username: str = Field(..., alias="username", validation_alias="loginId")
    email: str | None = Field(None, alias="email")
    name: str | None = Field(None, alias="name")
    last_name: str | None = Field(None, alias="lastName", validation_alias="lastName")
    status: bool = Field(False, alias="status", validation_alias="status", exclude=True)

    @field_validator('status', mode='before')
    @classmethod
    def validator_status(cls, v: Any):
        if v is not None:
            if isinstance(v, str):
                if v.lower() == "a":
                    return True
                elif v.lower() == "i":
                    return False
        return False

    @computed_field(alias="displayName")
    @property
    def display_name(self) -> str:
        return ' '.join([self.name, self.last_name])

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class UserWithPassword(User):
    hashed_password: str = Field(None, alias="hashedPassword", validation_alias="hashedPassword", exclude=True)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
