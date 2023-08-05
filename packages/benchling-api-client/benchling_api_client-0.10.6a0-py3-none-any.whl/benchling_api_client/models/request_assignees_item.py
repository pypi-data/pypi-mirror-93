from typing import Any, Dict, List, Union, cast

import attr

from ..models.team_summary import TeamSummary
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class RequestAssigneesItem:
    """  """

    team: Union[TeamSummary, Unset] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        team: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.team, Unset):
            team = self.team.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if team is not UNSET:
            field_dict["team"] = team

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "RequestAssigneesItem":
        d = src_dict.copy()
        team: Union[TeamSummary, Unset] = UNSET
        _team = d.pop("team", UNSET)
        if _team is not None and not isinstance(_team, Unset):
            team = TeamSummary.from_dict(cast(Dict[str, Any], _team))

        request_assignees_item = RequestAssigneesItem(
            team=team,
        )

        request_assignees_item.additional_properties = d
        return request_assignees_item

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
