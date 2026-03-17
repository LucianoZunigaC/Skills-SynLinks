from contextlib import asynccontextmanager
from io import BytesIO
from typing import List

from azure.storage.blob.aio import BlobServiceClient, BlobClient


class BlobRepository:
    def __init__(self, connection_string: str, container_name: str = 'DefaultContainer'):
        self.connection_string = connection_string
        self.container_name = container_name

    @asynccontextmanager
    async def _get_container_client(self):
        async with BlobServiceClient.from_connection_string(self.connection_string) as blob_service_client:
            container_client = blob_service_client.get_container_client(self.container_name)
            if not await container_client.exists():
                await container_client.create_container()
            yield container_client

    async def upload_blob(self, blob_name: str, blob_content: BytesIO) -> BlobClient:
        async with self._get_container_client() as container_client:
            blob_client = container_client.get_blob_client(blob_name)
            await blob_client.upload_blob(blob_content, overwrite=True)
            return blob_client

    async def download_blob(self, blob_name: str) -> BytesIO:
        async with self._get_container_client() as container_client:
            blob_client = container_client.get_blob_client(blob_name)
            downloader = await blob_client.download_blob()

            stream = BytesIO()
            await downloader.readinto(stream)
            stream.seek(0)

            return stream

    async def list_blobs(self) -> List[str]:
        async with self._get_container_client() as container_client:
            blobs_list = container_client.list_blobs()
            return [blob.name for blob in blobs_list]

    async def delete_blob(self, blob_name: str):
        async with self._get_container_client() as container_client:
            blob_client = container_client.get_blob_client(blob_name)
            await blob_client.delete_blob()
