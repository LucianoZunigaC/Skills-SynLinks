import asyncio
from typing import Sequence, Annotated

import pandas as pd
from fastapi import APIRouter, Depends, status, Header, UploadFile, HTTPException, Query

from .dependencies import get_package_service, get_upload_service, get_period_service
from .schemas import PackageMapping, UpdatePackageMapping, PackageFormAction, \
    ValidatePackageMapping, PackageMappingValidate, PackageDTO
from .services import PackageService, UploadService, PeriodService
from ..forms.dependencies import get_form_service, get_form_period_service
from ..forms.schemas import FormHistoryBase, FormRowDefinition, FormColumnDefinition, FormColumnGroupDefinition
from ..forms.services import FormService, FormPeriodService
from src.features.auth.dependencies import get_current_active_user
from src.features.auth.schemas import User
from ...shared.dependencies import get_blob_service
from ...shared.schemas import TreeNode
from ...shared.services.blob_service import BlobService

router = APIRouter()


@router.get("",
            status_code=status.HTTP_200_OK,
            response_model=Sequence[PackageDTO])
async def get_packages(current_user: User = Depends(get_current_active_user),
                       package_service: PackageService = Depends(get_package_service)):
    """
    Obtiene todos los paquetes disponibles.
    """
    return await package_service.get_packages_by_user_id(user_id=current_user.username)


@router.get("/tree",
            status_code=status.HTTP_200_OK,
            response_model=Sequence[TreeNode],
            response_model_exclude_none=True)
async def get_package_tree(
        accept_language: Annotated[str | None, Header()] = None,
        current_user: User = Depends(get_current_active_user),
        package_service: PackageService = Depends(get_package_service)):
    """
    Obtiene la estructura de árbol de paquetes.
    """
    return await package_service.get_packages_in_tree(user_id=current_user.username)


@router.post("/{package_id}/files")
async def upload_excel_file(package_id: str | int,
                            file: UploadFile,
                            current_user: User = Depends(get_current_active_user),
                            upload_service: UploadService = Depends(get_upload_service),
                            blob_service: BlobService = Depends(get_blob_service)):
    """
    Sube un archivo Excel y devuelve información sobre sus hojas de trabajo.
    """

    file_content = await file.read()
    excel_file = await upload_service.process_excel_upload(package_id=package_id, file_name=file.filename,
                                                           file_content_type=file.content_type,
                                                           file_content=file_content, user_id=current_user.username)

    return excel_file

@router.get("/{package_id}/mapping",
            status_code=status.HTTP_200_OK,
            response_model=Sequence[PackageMapping])
async def get_package_mapping(
        package_id: str | int,
        current_user: User = Depends(get_current_active_user),
        package_service: PackageService = Depends(get_package_service)):
    """
    Obtiene el mapeo de formularios para un paquete específico.
    """
    return await package_service.get_packages_mapping_by_id(package_id=package_id, user_id=current_user.username)



@router.post("/{package_id}/forms/{form_id}",
             status_code=status.HTTP_200_OK)
async def update_package_mapping(
        package_id: str | int,
        form_id: str | int,
        payload: UpdatePackageMapping,
        current_user: User = Depends(get_current_active_user),
        blob_service: BlobService = Depends(get_blob_service),
        form_service: FormService = Depends(get_form_service),
        package_service: PackageService = Depends(get_package_service),
        period_service: PeriodService = Depends(get_period_service),
        upload_service: UploadService = Depends(get_upload_service)):
    configs = await package_service.get_package_config_by_id(package_id=package_id, user_id=current_user.username)
    current_config = next((config for config in configs if str(config.form_id) == str(form_id)), None)
    if not current_config:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuración no encontrada")

    await asyncio.sleep(1)
    upload = await upload_service.get_upload(upload_id=payload.file_id)
    blob = await blob_service.download_file(upload.storage_url.split("/")[-1])

    df = pd.read_excel(blob, sheet_name=payload.sheet_name, header=current_config.import_query.header_row,
                       usecols=current_config.import_query.use_columns)

    period = await period_service.get_period(period_id=current_config.period_id)
    if payload.action is PackageFormAction.CREATE:
        if not await form_service.add_period(form_id=form_id, user_id=current_user):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuración no encontrada")

        period = await period_service.get_next_period(period_id=current_config.period_id)

    return await form_service.save_form_data_from_dataframe(form_id=form_id,
                                                            period_id=period.id,
                                                            user_id=current_user.username,
                                                            data=df)


@router.get("/{package_id}/forms/{form_id}/periods",
            status_code=status.HTTP_200_OK,
            response_model=Sequence[FormHistoryBase]
            )
async def get_package_mapping_periods(
        package_id: str | int,
        form_id: str | int,
        current_user: User = Depends(get_current_active_user),
        form_service: FormService = Depends(get_form_service),
        package_service: PackageService = Depends(get_package_service),
        period_service: FormPeriodService = Depends(get_form_period_service)):
    configs = await package_service.get_package_config_by_id(package_id=package_id, user_id=current_user.username)
    current_config = next((config for config in configs if str(config.form_id) == str(form_id)), None)
    if not current_config:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuración no encontrada")

    await asyncio.sleep(1)

    collection = []
    next_period = await form_service.get_next_period_by_id(form_id=form_id)
    if next_period is not None:
        collection.append(next_period)
    await asyncio.sleep(1)
    form_histories = await form_service.get_form_history_by_id(form_id=form_id)

    for history in form_histories:
        collection.append(FormHistoryBase.model_validate(history))
    return collection


@router.post("/{package_id}/forms/{form_id}/validate",
            status_code=status.HTTP_200_OK,
            )
async def validate_package_mapping_periods(
        package_id: str | int,
        form_id: str | int,
        payload: ValidatePackageMapping,
        current_user: User = Depends(get_current_active_user),
        blob_service: BlobService = Depends(get_blob_service),
        form_service: FormService = Depends(get_form_service),
        package_service: PackageService = Depends(get_package_service),
        period_service: FormPeriodService = Depends(get_form_period_service),
        upload_service: UploadService = Depends(get_upload_service)):
    if payload.sheet_name is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SheetName Not Found")
    if payload.file_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FileId Not Found")

    configs = await package_service.get_package_config_by_id(package_id=package_id, user_id=current_user.username)
    current_config = next((config for config in configs if str(config.form_id) == str(form_id)), None)
    if not current_config:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuración no encontrada")

    await asyncio.sleep(1)
    upload = await upload_service.get_upload(upload_id=payload.file_id)
    blob = await blob_service.download_file(upload.storage_url.split("/")[-1])

    try:
        df = pd.read_excel(blob, sheet_name=payload.sheet_name, header=current_config.import_query.header_row,
                           usecols=current_config.import_query.use_columns)

        # TODO: Agregar validacion de columnas o rango y tipo de datos
        return PackageMappingValidate(
            bulk_id=package_id,
            form_id=form_id,
            file_id=payload.file_id,
            sheet_name=payload.sheet_name,
            status='valid'
        )
    except Exception as e:
        return PackageMappingValidate(
            bulk_id=package_id,
            form_id=form_id,
            file_id=payload.file_id,
            sheet_name=payload.sheet_name,
            status='invalid'
        )

@router.get("/{package_id}/forms/{form_id}/periods/{period_id}/rows",
            status_code=status.HTTP_200_OK,
            response_model=Sequence[FormRowDefinition]
            )
async def get_package_form_period_rows(
        package_id: str | int,
        form_id: str | int,
        period_id: str | int,
        file_id: Annotated[str | int | None, Query(alias='fileId', max_length=50)] = None,
        sheet_name: Annotated[str | None, Query(alias='sheetName', max_length=50)] = None,
        current_user: User = Depends(get_current_active_user),
        blob_service: BlobService = Depends(get_blob_service),
        form_service: FormService = Depends(get_form_service),
        package_service: PackageService = Depends(get_package_service),
        period_service: FormPeriodService = Depends(get_form_period_service),
        upload_service: UploadService = Depends(get_upload_service)):
    configs = await package_service.get_package_config_by_id(package_id=package_id, user_id=current_user.username)
    current_config = next((config for config in configs if str(config.form_id) == str(form_id)), None)
    if not current_config:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuración no encontrada")

    await asyncio.sleep(1)
    upload = await upload_service.get_upload(upload_id=file_id)
    blob = await blob_service.download_file(upload.storage_url.split("/")[-1])

    df = pd.read_excel(blob, sheet_name=sheet_name, header=current_config.import_query.header_row,
                       usecols=current_config.import_query.use_columns)

    return await form_service.process_form_data(form_id=form_id, period_id=period_id, data=df)



@router.get("/{package_id}/forms/{form_id}/periods/{period_id}/columns",
            status_code=status.HTTP_200_OK,
            response_model=Sequence[FormColumnDefinition | FormColumnGroupDefinition],
            response_model_exclude_none=True
            )
async def get_package_form_period_columns(
        package_id: str | int,
        form_id: str | int,
        period_id: str | int,
        current_user: User = Depends(get_current_active_user),
        package_service: PackageService = Depends(get_package_service),
        form_service: FormService = Depends(get_form_service)):
    if not await package_service.form_includes_in_package(package_id=package_id, form_id=form_id,
                                                          user_id=current_user.username):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FileId Not Found")
    # TODO: Validar que el formulario pertenece a el package
    return await form_service.get_form_columns_by_id(form_id=form_id, period_id=period_id)
