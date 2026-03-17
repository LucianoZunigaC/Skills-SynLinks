from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class AzureStorageSettings(BaseSettings):
    # https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-tune-upload-download-python
    AZURE_STORAGE_CONNECTION_STRING: str = (
        Field(default='',
              validation_alias='AZURE_STORAGE_CONNECTION_STRING',
              description='A connection string to an Azure Storage account.'))
    AZURE_STORAGE_MAX_BLOCK_SIZE: int = (
        Field(default=4 * 1024 * 1024,
              validation_alias='AZURE_STORAGE_MAX_BLOCK_SIZE',
              description='The maximum chunk size for uploading a block blob in chunks.'))
    AZURE_STORAGE_MAX_SINGLE_PUT_SIZE: int = (
        Field(default=64 * 1024 * 1024,
              validation_alias='AZURE_STORAGE_MAX_SINGLE_PUT_SIZE',
              description='If the blob size is less than or equal max_single_put_size, then the blob will be uploaded '
                          'with only one http PUT request.'))
    AZURE_STORAGE_MIN_LARGE_BLOCK_UPLOAD_THRESHOLD: int = (
        Field(default=4 * 1024 * 1024,
              validation_alias='AZURE_STORAGE_MIN_LARGE_BLOCK_UPLOAD_THRESHOLD',
              description='The minimum chunk size required to use the memory efficient algorithm when uploading a '
                          'block blob.'))
    AZURE_STORAGE_USE_BYTE_BUFFER: bool = (
        Field(default=False,
              validation_alias='AZURE_STORAGE_USE_BYTE_BUFFER',
              description='Use a byte buffer for block blob uploads.'))
    AZURE_STORAGE_MAX_PAGE_SIZE: int = (
        Field(default=4 * 1024 * 1024,
              validation_alias='AZURE_STORAGE_MAX_PAGE_SIZE',
              description='The maximum chunk size for uploading a page blob.'))
    AZURE_STORAGE_MAX_SINGLE_GET_SIZE: int = (
        Field(default=32 * 1024 * 1024,
              validation_alias='AZURE_STORAGE_MAX_SINGLE_GET_SIZE',
              description='The maximum size for a blob to be downloaded in a single call, the exceeded part will be '
                          'downloaded in chunks (could be parallel).'))
    AZURE_STORAGE_MAX_CHUNK_GET_SIZE: int = (
        Field(default=4 * 1024 * 1024,
              validation_alias='AZURE_STORAGE_MAX_CHUNK_GET_SIZE',
              description='The maximum chunk size used for downloading a blob.'))
    AZURE_STORAGE_DEBUG: Optional[bool] = (
        Field(default=False,
              validation_alias='AZURE_STORAGE_DEBUG',
              description='Enables logging at the DEBUG level. Defaults to False. Can also be passed in at the client '
                          'level to enable it for all requests.'))
