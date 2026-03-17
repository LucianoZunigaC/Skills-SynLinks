from typing import Sequence, Annotated

from fastapi import APIRouter, Depends, Query
from starlette import status

from .dependencies import get_group_service
from .schemas import Group
from .services import GroupService
from ..forms.dependencies import get_form_service
from ..forms.schemas import Form, ExpandParams
from ..forms.services import FormService

router = APIRouter()


@router.get("",
             status_code=status.HTTP_200_OK,
            response_model=Sequence[Group])
async def get_groups(
        expand_query: Annotated[ExpandParams, Query()],
        group_service: GroupService = Depends(get_group_service)):
    return await group_service.get_all_groups()


@router.get("/{group_id}/forms",
             status_code=status.HTTP_200_OK,
            response_model=Sequence[Form])
async def get_forms_in_group(group_id: str,
                             group_service: GroupService = Depends(get_group_service),
                             form_service: FormService = Depends(get_form_service)):
    group = await group_service.get_group_by_id(group_id=group_id)

    forms = await form_service.get_forms_by_group_id(group_id=group_id)
    return forms
