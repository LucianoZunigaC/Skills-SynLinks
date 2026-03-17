from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import SettingsConfigDict

from src.settings import CORSSettings, OAuth2Settings, APISettings, AzureStorageSettings, SQLAlchemySettings

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
UPLOAD_DIR = STATIC_DIR / "uploads"


class AppSettings(APISettings, SQLAlchemySettings, CORSSettings, AzureStorageSettings, OAuth2Settings):
    PACKAGE_UPLOADS_CONTAINER_NAME: str = (
        Field(default='package-uploads',
              validation_alias='PACKAGE_UPLOADS_CONTAINER_NAME',
              description='The name of the container to use for package uploads.'))

    model_config = SettingsConfigDict(env_file='..env', env_file_encoding='utf-8', case_sensitive=True)


settings = AppSettings()
