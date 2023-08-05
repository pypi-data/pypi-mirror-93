from typing import Any, Dict, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class EntrySchema:
    """ Entry schema """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "EntrySchema":
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        entry_schema = EntrySchema(
            id=id,
            name=name,
        )

        return entry_schema
