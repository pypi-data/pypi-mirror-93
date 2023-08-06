from typing import Any, Dict, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class TeamSummary:
    """  """

    name: Union[Unset, str] = UNSET
    handle: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        handle = self.handle
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if handle is not UNSET:
            field_dict["handle"] = handle
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "TeamSummary":
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        handle = d.pop("handle", UNSET)

        id = d.pop("id", UNSET)

        team_summary = TeamSummary(
            name=name,
            handle=handle,
            id=id,
        )

        return team_summary
