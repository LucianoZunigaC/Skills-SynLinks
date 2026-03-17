from typing import Any, Sequence, Optional, Tuple


def is_valid_float(value: str) -> bool:
    """
    Check if a given string value can be converted to a float.

    Args:
        value (str): Value to check.

    Returns:
        bool: True if value is a valid float, False otherwise.
    """
    try:
        float(value)  # Attempt conversion to float
        return True
    except ValueError:
        return False


def is_valid_int(value: str) -> bool:
    """
    Check if a given string value can be converted to an integer.

    Args:
        value (str): Value to check.

    Returns:
        bool: True if value is a valid integer, False otherwise.
    """
    try:
        int(value)  # Attempt conversion to int
        return True
    except ValueError:
        return False


def field_validator_generic(v: Any,
                            true_values: Sequence[str] | str | None = None,
                            false_values: Sequence[str] | str | None = None,
                            default: bool | None = None) -> bool | None:
    """
    Validates a value and maps it based on the provided lists of valid values for True and False.

    :param v: The value to be validated.
    :param true_values: List or single string that should map to True (default is ['true']).
    :param false_values: List or single string that should map to False (default is ['false']).
    :param default: The default value to return if the value doesn't match any of the valid values (default is None).
    :return: True, False, or the default value if no match is found, or None.
    """
    if v is None:
        return None

    # Ensure true_values and false_values are lists, even if a single string is passed
    if isinstance(true_values, str):
        true_values = [true_values]
    if isinstance(false_values, str):
        false_values = [false_values]

    # Use default values if not provided
    if true_values is None:
        true_values = ['true']
    if false_values is None:
        false_values = ['false']

    if isinstance(v, str):
        lower_v = v.lower()
        # Convert the lists to lowercase for case-insensitive matching
        true_values_lower = [value.lower() for value in true_values]
        false_values_lower = [value.lower() for value in false_values]

        if lower_v in true_values_lower:
            return True
        elif lower_v in false_values_lower:
            return False

    return default


def unpack_group_key(group_key: Optional[Tuple]) -> Tuple[Optional[int], Optional[str]]:
    """
    Unpacks a group key into its `group_id` and `group_name`.

    Args:
        group_key (Optional[Tuple]): Group key that should be a tuple with at least two elements.

    Returns:
        Tuple[Optional[int], Optional[str]]: A tuple with `group_id` and `group_name`.
                                             If the key is invalid, returns `(None, None)`.
    """
    if group_key is not None and isinstance(group_key, tuple) and len(group_key) >= 2:
        return group_key[0], group_key[-1]  # Extraer group_id y group_name de la tupla
    return None, None  # Retornar None si la clave no es válida
