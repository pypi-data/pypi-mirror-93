from typing import Any, Dict, List, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class EntrySchemaDetailedOrganization:
    """The organization that owns the schema."""

    handle: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        handle = self.handle
        id = self.id
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if handle is not UNSET:
            field_dict["handle"] = handle
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "EntrySchemaDetailedOrganization":
        d = src_dict.copy()
        handle = d.pop("handle", UNSET)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        entry_schema_detailed_organization = EntrySchemaDetailedOrganization(
            handle=handle,
            id=id,
            name=name,
        )

        entry_schema_detailed_organization.additional_properties = d
        return entry_schema_detailed_organization

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
