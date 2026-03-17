from enum import StrEnum


class STATUS(StrEnum):
    ACTIVE = "A"
    INACTIVE = "I"


class TypeCode(StrEnum):
    INTEGER = "INT"
    DECIMAL = "DEC"
    FLOAT = "FLOAT"
    TEXT = "TEXT"
    BOOLEAN = "BOOLEAN"
    DATETIME = "DATETIME"
