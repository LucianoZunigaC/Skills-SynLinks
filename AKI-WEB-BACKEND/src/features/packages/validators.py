from fastapi import HTTPException, status

from src.features.packages.config import SUPPORTED_EXTENSIONS, SUPPORTED_MIME_TYPES


def validate_file_extension(file_extension: str):
    """
    Valida que la extensión del archivo esté soportada (case insensitive).
    """
    if file_extension.lower() not in [ext.lower() for ext in SUPPORTED_EXTENSIONS]:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file extension. Allowed extensions: {', '.join(SUPPORTED_EXTENSIONS)}"
        )


def validate_mime_type(content_type: str):
    """
    Valida que el tipo MIME del archivo esté soportado (case insensitive).
    """
    if content_type.lower() not in [mime.lower() for mime in SUPPORTED_MIME_TYPES]:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported media type. Allowed types: {', '.join(SUPPORTED_MIME_TYPES)}"
        )
