from datetime import datetime
from io import BytesIO
from typing import Annotated, TypeVar, Union, Sequence

import aiofiles
import orjson
import pandas as pd
from fastapi import APIRouter, status, UploadFile, File, HTTPException, Body
from fastapi.responses import ORJSONResponse

from src.config import UPLOAD_DIR
from src.features.pandas.schemas import SheetInfo, ExcelFileInfo, ExcelReadOptions
from src.features.pandas.utils import read_excel_sheet, dataframe_to_json, get_file_path

router = APIRouter()


@router.post("/sheet-names",
             status_code=status.HTTP_200_OK,
             response_model=ExcelFileInfo)
async def get_sheet_names(file: Annotated[UploadFile, File()]):
    # Leer el archivo Excel cargado como un objeto en memoria
    contents = await file.read()

    # Utilizar pandas para obtener la lista de hojas (sheet names)
    excel_file = pd.ExcelFile(BytesIO(contents))

    # Obtener información sobre cada hoja
    sheets_info = [
        SheetInfo(
            name=sheet_name,
            num_rows=len(pd.read_excel(excel_file, sheet_name=sheet_name)),
            num_columns=len(pd.read_excel(excel_file, sheet_name=sheet_name, nrows=0).columns)
        )
        for sheet_name in excel_file.sheet_names
    ]

    # Devolver un objeto que incluye toda la información
    return ExcelFileInfo(
        file_name=file.filename,
        total_sheets=len(excel_file.sheet_names),
        creation_date=datetime.now().isoformat(),  # Simulando la fecha de creación
        modification_date=datetime.now().isoformat(),  # Simulando la fecha de modificación
        file_type=file.content_type,  # Tipo de archivo
        sheet_names=excel_file.sheet_names,
        sheets_info=sheets_info
    )


@router.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    # Crear la carpeta de subidas si no existe
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    file_location = UPLOAD_DIR / file.filename

    async with aiofiles.open(file_location, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)
    return {"filename": file.filename}


@router.post("/read-excel/{file_name}",
             status_code=status.HTTP_200_OK)
async def read_excel(file_name: str,
                     payload: Annotated[Sequence[ExcelReadOptions] | None, Body(...)] = None):
    try:
        file_path = get_file_path(file_name)
        excel_file = pd.ExcelFile(file_path)

        results = []

        if payload is None:
            df = read_excel_sheet(excel_file)
            results.append(dataframe_to_json(df))
        else:
            for options in payload:
                df = read_excel_sheet(excel_file, options)
                results.append(dataframe_to_json(df))

        return ORJSONResponse(content=results)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"File not found or error reading file: {str(e)}")
