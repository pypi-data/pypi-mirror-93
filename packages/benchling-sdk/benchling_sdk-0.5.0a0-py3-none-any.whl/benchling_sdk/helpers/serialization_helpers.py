from typing import Any, Dict, Iterable, Optional, TypeVar, Union

from benchling_api_client.models.custom_fields import CustomFields
from benchling_api_client.models.fields import Fields
from benchling_api_client.models.schema_fields_query_param import SchemaFieldsQueryParam
from benchling_api_client.types import Unset, UNSET

T = TypeVar("T")


def optional_array_query_param(inputs: Optional[Iterable[str]]) -> Optional[str]:
    if inputs:
        return array_query_param(inputs)
    return None


def array_query_param(inputs: Iterable[str]) -> str:
    return ",".join(inputs)


def fields(source: Dict[str, Any]) -> Fields:
    """Marshals a dictionary into a Fields object"""
    return Fields.from_dict(source)


def custom_fields(source: Dict[str, Any]) -> CustomFields:
    """Marshals a dictionary into a CustomFields object"""
    return CustomFields.from_dict(source)


def unset_as_none(source: Union[Unset, None, T]) -> Optional[T]:
    """Given a value that may be UNSET, produces an Optional[] where UNSET will be treated as None"""
    if source is UNSET:
        return None
    return source  # type: ignore


def schema_fields_query_param(schema_fields: Optional[Dict[str, Any]]) -> Optional[SchemaFieldsQueryParam]:
    return (
        SchemaFieldsQueryParam.from_dict(
            {f"schemaField.{field}": value for field, value in schema_fields.items()}
        )
        if schema_fields
        else None
    )
