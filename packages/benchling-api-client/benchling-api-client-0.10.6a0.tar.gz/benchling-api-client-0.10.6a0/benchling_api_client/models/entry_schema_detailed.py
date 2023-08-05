from typing import Any, Dict, List, Union, cast

import attr

from ..models.entry_schema_detailed_organization import EntrySchemaDetailedOrganization
from ..models.entry_schema_detailed_type import EntrySchemaDetailedType
from ..models.schema_field import SchemaField
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class EntrySchemaDetailed:
    """  """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    prefix: Union[Unset, str] = UNSET
    registry_id: Union[Unset, str] = UNSET
    field_definitions: Union[Unset, List[SchemaField]] = UNSET
    type: Union[Unset, EntrySchemaDetailedType] = UNSET
    organization: Union[EntrySchemaDetailedOrganization, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        prefix = self.prefix
        registry_id = self.registry_id
        field_definitions: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.field_definitions, Unset):
            field_definitions = []
            for field_definitions_item_data in self.field_definitions:
                field_definitions_item = field_definitions_item_data.to_dict()

                field_definitions.append(field_definitions_item)

        type: Union[Unset, EntrySchemaDetailedType] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type

        organization: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.organization, Unset):
            organization = self.organization.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if prefix is not UNSET:
            field_dict["prefix"] = prefix
        if registry_id is not UNSET:
            field_dict["registryId"] = registry_id
        if field_definitions is not UNSET:
            field_dict["fieldDefinitions"] = field_definitions
        if type is not UNSET:
            field_dict["type"] = type
        if organization is not UNSET:
            field_dict["organization"] = organization

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "EntrySchemaDetailed":
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        prefix = d.pop("prefix", UNSET)

        registry_id = d.pop("registryId", UNSET)

        field_definitions = []
        _field_definitions = d.pop("fieldDefinitions", UNSET)
        for field_definitions_item_data in _field_definitions or []:
            field_definitions_item = SchemaField.from_dict(field_definitions_item_data)

            field_definitions.append(field_definitions_item)

        type = None
        _type = d.pop("type", UNSET)
        if _type is not None:
            type = EntrySchemaDetailedType(_type)

        organization: Union[EntrySchemaDetailedOrganization, Unset] = UNSET
        _organization = d.pop("organization", UNSET)
        if _organization is not None and not isinstance(_organization, Unset):
            organization = EntrySchemaDetailedOrganization.from_dict(cast(Dict[str, Any], _organization))

        entry_schema_detailed = EntrySchemaDetailed(
            id=id,
            name=name,
            prefix=prefix,
            registry_id=registry_id,
            field_definitions=field_definitions,
            type=type,
            organization=organization,
        )

        return entry_schema_detailed
