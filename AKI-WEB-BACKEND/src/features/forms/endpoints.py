from io import BytesIO
from typing import Sequence, Annotated

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body, UploadFile, File, Header
from starlette.responses import StreamingResponse

from src.features.pandas.utils import read_excel_sheet
from .dependencies import get_form_service, get_form_period_service
from .mappings import map_period_to_list_item, process_form_entry
from .schemas import Form, FormBase, FormColumnDefinition, FormHistory, FormEntry, FormRowDefinition, \
    FormColumnGroupDefinition
from .services import FormService, FormPeriodService
from src.features.auth.dependencies import get_current_active_user
from src.features.auth.schemas import User
from ...shared.schemas import ListItem, TreeNode

router = APIRouter()


@router.get("",
            status_code=status.HTTP_200_OK,
            response_model=Sequence[Form])
async def get_forms(form_service: FormService = Depends(get_form_service)):
    return await form_service.get_all_form()


@router.get("/tree",
            status_code=status.HTTP_200_OK,
            response_model=Sequence[TreeNode],
            response_model_exclude_none=True)
async def get_forms_by_user_id(accept_language: Annotated[str | None, Header()] = None,
                               current_user: User = Depends(get_current_active_user),
                               form_service: FormService = Depends(get_form_service)):
    return await form_service.get_forms_in_tree(user_id=current_user.username, language_id=1)


@router.get("/{form_id}",
            status_code=status.HTTP_200_OK,
            response_model=FormBase)
async def get_form_by_id(form_id: str, form_service: FormService = Depends(get_form_service)):
    item = await form_service.get_form_by_id(form_id=form_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Form not found")
    return item


@router.get("/{form_id}/periods",
            status_code=status.HTTP_200_OK,
            response_model=Sequence[ListItem])
async def get_periods_for_form_id(form_id: str, period_service: FormPeriodService = Depends(get_form_period_service)):
    collection = await period_service.get_periods_by_form(form_id=form_id)

    return [map_period_to_list_item(item) for item in collection]


@router.get("/{form_id}/periods/{period_id}/columns",
            status_code=status.HTTP_200_OK,
            response_model=Sequence[FormColumnDefinition | FormColumnGroupDefinition],
            response_model_exclude_none=True)
async def get_form_column_definitions_by_id(form_id: int,
                                            period_id: str | int | None = 'latest',
                                            form_service: FormService = Depends(get_form_service)):
    return await form_service.get_form_columns_by_id(form_id=form_id, period_id=period_id)


@router.get("/{form_id}/periods/{period_id}/data",
            status_code=status.HTTP_200_OK,
            response_model=Sequence[FormRowDefinition])
async def get_form_data_by_id(form_id: int,
                              period_id: str | int | None = 'latest',
                              current_user: User = Depends(get_current_active_user),
                              form_service: FormService = Depends(get_form_service)):
    return await form_service.get_form_rows_by_id(form_id=form_id, period_id=period_id, user_id=current_user.username)


@router.post("/{form_id}/periods/{period_id}/data",
             status_code=status.HTTP_201_CREATED)
async def save_form_data_by_id(form_id: str | int,
                               period_id: str | int | None = 'latest',
                               payload: Annotated[Sequence[FormEntry] | None, Body()] = None,
                               form_service: FormService = Depends(get_form_service)):
    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Body cannot be empty or null.")

    if not period_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Period cannot be empty or null.")

    entities = await form_service.get_form_raw_by_id(form_id=form_id, period_id=period_id)

    create_form_data_list = []
    for entry in payload:
        processed_data = process_form_entry(entry, entities)
        create_form_data_list.extend(processed_data)

    return await form_service.save_form_data(create_form_data_list)


@router.get("/{form_id}/history",
            status_code=status.HTTP_200_OK,
            response_model=Sequence[FormHistory])
async def get_form_history_by_id(form_id: int,
                                 form_service: FormService = Depends(get_form_service)):
    return await form_service.get_form_history_by_id(form_id=form_id)




@router.get('/{form_id}/periods/{period_id}/export',
            status_code=status.HTTP_200_OK)
async def download_file(form_id: int,
                        period_id: int,
                        language: Annotated[str | None, Query()] = None,
                        current_user: User = Depends(get_current_active_user),
                        form_service: FormService = Depends(get_form_service)):
    output = await form_service.export_form_data_to_excel(form_id=form_id, period_id=period_id,
                                                          user_id=current_user.username)

    # Crear una respuesta de streaming
    return StreamingResponse(output,
                             media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                             headers={
                                 "Content-Disposition": f"attachment; filename=form_{form_id}_perdiod_{period_id}.xlsx"})


@router.post('/{form_id}/periods/{period_id}/upload',
             status_code=status.HTTP_200_OK)
async def upload_file(form_id: int,
                      period_id: str | int | None = 'latest',
                      file: UploadFile = File(...),
                      form_service: FormService = Depends(get_form_service)):
    contents = await file.read()
    excel_file = pd.ExcelFile(BytesIO(contents))
    df = read_excel_sheet(excel_file)

    return await form_service.process_form_data(form_id=form_id, period_id=period_id, data=df)


@router.post('/{form_id}/periods',
             status_code=status.HTTP_201_CREATED)
async def add_period(form_id: int,
                     current_user: User = Depends(get_current_active_user),
                     form_service: FormService = Depends(get_form_service)):
    await form_service.add_period(form_id=form_id, user_id=current_user.username)
