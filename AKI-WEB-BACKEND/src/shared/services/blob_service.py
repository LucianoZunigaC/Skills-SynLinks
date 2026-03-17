from io import BytesIO

from src.shared.repositories.blob_repository import BlobRepository


class BlobService:
    """Service class for handling blob storage operations."""

    def __init__(self, repository: BlobRepository):
        """Initialize BlobService with a repository.
        
        Args:
            repository (BlobRepository): Repository instance for blob operations
        """
        self.repository = repository

    async def upload_file(self, file_name: str, file_content: BytesIO) -> str:
        """Upload a file to blob storage.
        
        Args:
            file_name (str): Name of the file to upload
            file_content (BytesIO): Content of the file as bytes
            
        Returns:
            str: URL of the uploaded blob
        """
        blob = await self.repository.upload_blob(file_name, file_content)
        return blob.url

    async def download_file(self, file_name: str) -> BytesIO:
        """Download a file from blob storage.
        
        Args:
            file_name (str): Name of the file to download
            
        Returns:
            BytesIO: Content of the downloaded file
        """
        blob_content = await self.repository.download_blob(file_name)
        return blob_content

    async def list_files(self) -> list[str]:
        """List all files in blob storage.
        
        Returns:
            list[str]: List of file names
        """
        return await self.repository.list_blobs()

    async def delete_file(self, file_name: str):
        """Delete a file from blob storage.
        
        Args:
            file_name (str): Name of the file to delete
        """
        await self.repository.delete_blob(file_name)
