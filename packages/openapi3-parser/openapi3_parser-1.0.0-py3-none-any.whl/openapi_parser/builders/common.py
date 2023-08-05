from collections import namedtuple
from typing import Any, Callable, Dict, Optional

from ..errors import ParserError

PropertyMeta = namedtuple('PropertyMeta', ['cast', 'name'])


def extract_typed_props(data: dict, attrs_map: Dict[str, PropertyMeta]) -> Dict[str, Any]:
    """Extract properties from the dictionary with type-casting using passed mapping

    Args:
        data (dict): Original dictionary to process
        attrs_map (Dict[str, PropertyMeta]): Type-casting mapping

    Returns:
         Dict[str, Any]: Dictionary with type-casted values
    """

    def cast_value(name: str, value: Any, type_cast_func: Optional[Callable]) -> Any:
        try:
            return type_cast_func(value) \
                if type_cast_func is not None \
                else value
        except ValueError:
            raise ParserError(f"Invalid value for '{name}' property, got '{value}'")

    custom_attrs = {
        attr_name: cast_value(attr_info.name, data[attr_info.name], attr_info.cast)
        for attr_name, attr_info in attrs_map.items()
        if data.get(attr_info.name) is not None
    }

    return custom_attrs


def merge_schema(original: dict, other: dict) -> dict:
    """Merge two schema dictionaries into single dict

    Args:
        original (dict): Source schema dictionary
        other (dict): Schema dictionary to append to the source

    Returns:
        dict: Dictionary value of new merged schema
    """
    source = original.copy()

    for key, value in other.items():
        if key not in source:
            source[key] = value
        else:
            if isinstance(value, list):
                source[key].extend(value)
            elif isinstance(value, dict):
                source[key] = merge_schema(source[key], value)
            else:
                source[key] = value

    return source


def extract_extension_attributes(schema: dict) -> dict:
    """Extract custom 'x-*' attributes from schema dictionary

    Args:
        schema (dict): Schema dictionary

    Returns:
        dict: Dictionary with parsed attributes w/o 'x-' prefix
    """
    extension_key_format = 'x-'

    extensions_dict: dict = {
        key.replace(extension_key_format, '').replace('-', '_'): value
        for key, value in schema.items()
        if key.startswith(extension_key_format)
    }

    return extensions_dict
