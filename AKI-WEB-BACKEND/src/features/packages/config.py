# Lista de extensiones y tipos MIME soportados por pd.ExcelFile
SUPPORTED_EXTENSIONS = [".xlsx", ".xls", ".xlsm", ".xlsb"]
SUPPORTED_MIME_TYPES = [
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # .xlsx
    "application/vnd.ms-excel",  # .xls
    "application/vnd.ms-excel.sheet.macroEnabled.12",  # .xlsm
    "application/vnd.ms-excel.sheet.binary.macroEnabled.12",  # .xlsb
]

DEFAULT_GROUP_ID = -1
DEFAULT_GROUP_NAME = 'Default'
