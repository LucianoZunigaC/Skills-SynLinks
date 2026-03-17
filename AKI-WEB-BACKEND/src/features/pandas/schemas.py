from typing import Sequence

from pydantic import BaseModel, Field, ConfigDict


class SheetInfo(BaseModel):
    name: str = Field(..., alias="sheetName")
    num_rows: int = Field(..., alias="numRows")
    num_columns: int = Field(..., alias="numColumns")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ExcelFileInfo(BaseModel):
    file_name: str = Field(..., alias="fileName")
    total_sheets: int = Field(..., alias="totalSheets")
    creation_date: str = Field(..., alias="creationDate")
    modification_date: str = Field(..., alias="modificationDate")
    file_type: str = Field(..., alias="fileType")
    sheet_names: Sequence[str] = Field(..., alias="sheetNames")
    sheets_info: Sequence[SheetInfo] = Field(..., alias="sheetsInfo")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ExcelReadOptions(BaseModel):
    sheet_name: int | str = Field(
        default=0,
        alias='sheetName',
        description='The name or index of the sheet to read. Default is the first sheet.'
    )
    header_row: int | Sequence[int] | None = Field(
        default=0,
        alias='headerRow',
        description='Row(s) to use as the column names. Default is the first row.'
    )
    column_names: Sequence[str] | None = Field(
        default=None,
        alias='columnNames',
        description='List of column names to use. Overrides the header row.'
    )
    columns_to_use: int | str | Sequence[int] | Sequence[str] | None = Field(
        default=None,
        alias='columnsToUse',
        description='Columns to read. Default is None, which reads all columns.'
    )
    # true_value_strings: Optional[List[str]] = Field(
    #     default=None,
    #     alias='trueValueStrings',
    #     description='Values to consider as True.'
    # )
    # false_value_strings: Optional[List[str]] = Field(
    #     default=None,
    #     alias='falseValueStrings',
    #     description='Values to consider as False.'
    # )
    rows_to_skip: int | Sequence[int] | None = Field(
        default=None,
        alias='rowsToSkip',
        description='Rows to skip at the start of the file.'
    )
    number_of_rows: int | None = Field(
        default=None,
        alias='numberOfRows',
        description='Number of rows to read from the file.'
    )
    # additional_na_values: Optional[Union[str, List[str], Dict[str, Any]]] = Field(
    #     default=None,
    #     alias='additionalNaValues',
    #     description='Additional strings to recognize as NA/NaN.'
    # )
    # keep_default_na: Optional[bool] = Field(
    #     default=True,
    #     alias='keepDefaultNa',
    #     description='Whether to keep the default NA values.'
    # )
    # detect_missing_values: Optional[bool] = Field(
    #     default=True,
    #     alias='detectMissingValues',
    #     description='Whether to detect missing values.'
    # )
    # parse_dates: Optional[Union[bool, List[Union[int, str]], Dict[str, List[Union[int, str]]]]] = Field(
    #     default=False,
    #     alias='parseDates',
    #     description='Whether to parse dates in the specified columns.'
    # )
    # date_format: Optional[Union[str, Dict[str, str]]] = Field(
    #     default=None,
    #     alias='dateFormat',
    #     description='Format to parse dates.'
    # )
    # thousands_separator: Optional[str] = Field(
    #     default=None,
    #     alias='thousandsSeparator',
    #     description='Character to recognize as thousands.'
    # )
    # decimal_separator: Optional[str] = Field(
    #     default='.',
    #     alias='decimalSeparator',
    #     description='Character to recognize as decimal.'
    # )
    footer_rows_to_skip: int | None = Field(
        default=0,
        alias='footerRowsToSkip',
        description='Number of lines at bottom of file to skip.'
    )

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
