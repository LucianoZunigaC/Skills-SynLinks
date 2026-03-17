from fastapi import Depends

from .services import UserService
from src.features.auth.dependencies import get_user_repository
from src.features.auth.repositories import UserRepository


async def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    yield UserService(user_repository)
