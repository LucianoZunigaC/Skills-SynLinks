from fastapi import APIRouter, status, Depends, HTTPException

from src.features.auth.schemas import User
from src.features.users.dependencies import get_user_service
from src.features.users.schemas import UserCreate
from src.features.users.services import UserService

router = APIRouter()

@router.post("", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user_in: UserCreate, user_service: UserService = Depends(get_user_service)):
    user = await user_service.get_user(username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered"
        )
    user = await user_service.get_user_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    return await user_service.create_user(user_in)
