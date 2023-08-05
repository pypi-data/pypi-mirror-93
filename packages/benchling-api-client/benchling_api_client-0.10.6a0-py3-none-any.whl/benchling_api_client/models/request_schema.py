from typing import Any, Dict, List, Optional, Union, cast

import attr

from ..models.request_schema_organization import RequestSchemaOrganization
from ..models.request_schema_type import RequestSchemaType
from ..models.schema_field import SchemaField
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class RequestSchema:
    """  """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    field_definitions: Union[Unset, List[SchemaField]] = UNSET
    type: Union[Unset, RequestSchemaType] = UNSET
    system_name: Union[Unset, str] = UNSET
    organization: Union[RequestSchemaOrganization, Unset] = UNSET
    sql_id: Union[Unset, Optional[str]] = UNSET
    derived_from: Union[Unset, Optional[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        field_definitions: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.field_definitions, Unset):
            field_definitions = []
            for field_definitions_item_data in self.field_definitions:
                field_definitions_item = field_definitions_item_data.to_dict()

                field_definitions.append(field_definitions_item)

        type: Union[Unset, RequestSchemaType] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type

        system_name = self.system_name
        organization: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.organization, Unset):
            organization = self.organization.to_dict()

        sql_id = self.sql_id
        derived_from = self.derived_from

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if field_definitions is not UNSET:
            field_dict["fieldDefinitions"] = field_definitions
        if type is not UNSET:
            field_dict["type"] = type
        if system_name is not UNSET:
            field_dict["systemName"] = system_name
        if organization is not UNSET:
            field_dict["organization"] = organization
        if sql_id is not UNSET:
            field_dict["sqlId"] = sql_id
        if derived_from is not UNSET:
            field_dict["derivedFrom"] = derived_from

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "RequestSchema":
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        field_definitions = []
        _field_definitions = d.pop("fieldDefinitions", UNSET)
        for field_definitions_item_data in _field_definitions or []:
            field_definitions_item = SchemaField.from_dict(field_definitions_item_data)

            field_definitions.append(field_definitions_item)

        type = None
        _type = d.pop("type", UNSET)
        if _type is not None:
            type = RequestSchemaType(_type)

        system_name = d.pop("systemName", UNSET)

        organization: Union[RequestSchemaOrganization, Unset] = UNSET
        _organization = d.pop("organization", UNSET)
        if _organization is not None and not isinstance(_organization, Unset):
            organization = RequestSchemaOrganization.from_dict(cast(Dict[str, Any], _organization))

        sql_id = d.pop("sqlId", UNSET)

        derived_from = d.pop("derivedFrom", UNSET)

        request_schema = RequestSchema(
            id=id,
            name=name,
            field_definitions=field_definitions,
            type=type,
            system_name=system_name,
            organization=organization,
            sql_id=sql_id,
            derived_from=derived_from,
        )

        return request_schema
