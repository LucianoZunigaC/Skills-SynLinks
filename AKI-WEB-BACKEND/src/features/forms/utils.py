import logging
from typing import Any, Dict, List

import pandas as pd
from pandas.io.formats import excel


def remove_bold_and_borders_excel_cell():
    try:
        # to remove bold and borders from the cell
        excel.ExcelFormatter.header_style = None
    except Exception as err:
        logging.error(err)


def filter_dataframe(dataframe: pd.DataFrame, criteria: dict, column_mapping: dict) -> pd.DataFrame:
    """
    Filters the DataFrame using the columns from the mapping with the keys from the criteria dictionary.

    :param dataframe: DataFrame to be filtered.
    :param criteria: Dictionary containing keys.
    :param column_mapping: Dictionary that maps DataFrame columns to keys in the criteria.
    :return: Filtered DataFrame.
    """
    # Lista de condiciones para filtrar el DataFrame
    filter_conditions = []

    # Obtener las columnas presentes en el DataFrame
    dataframe_columns = dataframe.columns

    # Iterar sobre el mapeo de columnas
    for column, keys in column_mapping.items():
        # Verificar si la columna está en el DataFrame
        if column not in dataframe_columns:
            continue  # Omitir la columna si no existe en el DataFrame

        # Filtrar las claves que están presentes en el criteria
        valid_keys = [key for key in keys if key in criteria]

        # Si hay claves válidas presentes en el criteria, creamos la condición
        if valid_keys:
            filter_conditions.append(dataframe[column].isin([criteria[key] for key in valid_keys]))

    # Combinamos todas las condiciones con 'or' lógico
    if filter_conditions:
        combined_filter_condition = filter_conditions[0]
        for condition in filter_conditions[1:]:
            combined_filter_condition = combined_filter_condition | condition

        # Filtrar el DataFrame usando la condición combinada
        filtered_dataframe = dataframe[combined_filter_condition]
    else:
        # Si no hay condiciones, retornar el DataFrame original sin filtrar
        filtered_dataframe = dataframe

    return filtered_dataframe


def get_valid_column(item: Dict[str, Any], column_names: List[str], column_value_mapping: List[str]) -> Any | None:
    """
    Returns the first valid column name from the column_value_mapping that exists in the item and column names provided.

    :param item: Dictionary containing potential column names and values.
    :param column_names: List of column names to check.
    :param column_value_mapping: List of column names to check against the item.
    :return: Valid column name if found, otherwise None.
    """
    for name in column_value_mapping:
        value = item.get(name, None)
        # Verificar si el valor es válido y existe en los nombres de columnas proporcionados
        if value and value in column_names:
            return value
    return None
