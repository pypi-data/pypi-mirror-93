from typing import Any, Dict, List, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class RequestWriteBaseAssigneesItem:
    """  """

    team_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        team_id = self.team_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if team_id is not UNSET:
            field_dict["teamId"] = team_id

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "RequestWriteBaseAssigneesItem":
        d = src_dict.copy()
        team_id = d.pop("teamId", UNSET)

        request_write_base_assignees_item = RequestWriteBaseAssigneesItem(
            team_id=team_id,
        )

        request_write_base_assignees_item.additional_properties = d
        return request_write_base_assignees_item

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
