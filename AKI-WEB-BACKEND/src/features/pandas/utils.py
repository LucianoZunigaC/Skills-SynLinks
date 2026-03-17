from pathlib import Path

import orjson
import pandas as pd

from src.config import UPLOAD_DIR
from src.features.pandas.schemas import ExcelReadOptions


def get_file_path(file_name: str) -> Path:
    """
    Construye la ruta completa del archivo basado en su nombre.
    Verifica que el archivo exista y sea un archivo válido.
    """
    file_path = UPLOAD_DIR / file_name
    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"File {file_name} not found")
    return file_path


def read_excel_sheet(excel_file: pd.ExcelFile, options: ExcelReadOptions | None = None) -> pd.DataFrame:
    """
    Lee una hoja de un archivo Excel según la configuración proporcionada.
    """
    if options is None:
        options = ExcelReadOptions()

    df = pd.read_excel(
        excel_file,
        sheet_name=options.sheet_name,
        header=options.header_row,
        names=options.column_names,
        usecols=options.columns_to_use,
        skiprows=options.rows_to_skip,
        nrows=options.number_of_rows,
        skipfooter=options.footer_rows_to_skip,
    )
    return df


def dataframe_to_json(df: pd.DataFrame) -> list[dict]:
    """
    Convierte un DataFrame de pandas en una lista de diccionarios JSON.
    """
    return orjson.loads(df.to_json(orient='records'))
