from fastapi import APIRouter, status, Depends

from ...auth.dependencies import get_current_active_user
from ...auth.schemas import User

router = APIRouter()


@router.get("/me",
             status_code=status.HTTP_200_OK,
             response_model=User)
async def get_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user
