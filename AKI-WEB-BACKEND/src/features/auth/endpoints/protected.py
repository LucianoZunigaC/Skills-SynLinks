from fastapi import APIRouter, status, Depends

from ..dependencies import get_current_active_user
from ..schemas import User

router = APIRouter()


@router.get("/userinfo",
             status_code=status.HTTP_200_OK,
             response_model=User)
async def get_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/sign-out",
             status_code=status.HTTP_204_NO_CONTENT,
             response_model=None)
async def get_user_me(current_user: User = Depends(get_current_active_user)):
    return None
