import secrets

from pydantic import Field
from pydantic_settings import BaseSettings


class OAuth2Settings(BaseSettings):
    secret_key: str = (
        Field(default=secrets.token_hex(32),
              validation_alias='SECRET_KEY',
              description='Secret key used for JWT token encoding and validation'))

    algorithm: str | None = (
        Field(default="HS256",
              validation_alias='ALGORITHM',
              description='A list of origins that should be permitted to make cross-origin requests.'))

    access_token_expire_minutes: float = (
        Field(default=30,
              validation_alias='ACCESS_TOKEN_EXPIRE_MINUTES',
              description='A list of origins that should be permitted to make cross-origin requests.'))
