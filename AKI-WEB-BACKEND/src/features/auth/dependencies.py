from typing import Annotated

from fastapi import Depends, HTTPException, status

from .repositories import UserRepository
from .schemas import User
from src.shared.security import oauth2_scheme
from .services import AuthService
from src.config import settings
from src.core import AsyncSessionDep


async def get_user_repository(session: AsyncSessionDep):
    yield UserRepository(session)


async def get_auth_service(user_repository: UserRepository = Depends(get_user_repository)):
    yield AuthService(user_repository=user_repository,
                      access_token_expire_minutes=settings.access_token_expire_minutes,
                      secret_key=settings.secret_key,
                      algorithm=settings.algorithm)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           auth_service: AuthService = Depends(get_auth_service)):
    token_data = auth_service.validate_token(token)

    user = await auth_service.get_user(token_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.status:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
