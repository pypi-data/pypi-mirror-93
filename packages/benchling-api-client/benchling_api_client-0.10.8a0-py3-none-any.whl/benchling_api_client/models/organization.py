from typing import Any, Dict, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class Organization:
    """  """

    handle: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        handle = self.handle
        id = self.id
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if handle is not UNSET:
            field_dict["handle"] = handle
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "Organization":
        d = src_dict.copy()
        handle = d.pop("handle", UNSET)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        organization = Organization(
            handle=handle,
            id=id,
            name=name,
        )

        return organization
