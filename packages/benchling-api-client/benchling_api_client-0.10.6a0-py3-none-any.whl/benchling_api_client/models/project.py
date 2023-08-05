from typing import Any, Dict, Union, cast

import attr

from ..models.organization import Organization
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class Project:
    """  """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    owner: Union[Unset, Organization, UserSummary] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        owner: Union[Unset, Organization, UserSummary]
        if isinstance(self.owner, Unset):
            owner = UNSET
        elif isinstance(self.owner, Organization):
            owner = UNSET
            if not isinstance(self.owner, Unset):
                owner = self.owner.to_dict()

        else:
            owner = UNSET
            if not isinstance(self.owner, Unset):
                owner = self.owner.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if owner is not UNSET:
            field_dict["owner"] = owner

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "Project":
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        def _parse_owner(data: Any) -> Union[Unset, Organization, UserSummary]:
            data = None if isinstance(data, Unset) else data
            owner: Union[Unset, Organization, UserSummary]
            try:
                owner = UNSET
                _owner = data
                if _owner is not None and not isinstance(_owner, Unset):
                    owner = Organization.from_dict(cast(Dict[str, Any], _owner))

                return owner
            except:  # noqa: E722
                pass
            owner = UNSET
            _owner = data
            if _owner is not None and not isinstance(_owner, Unset):
                owner = UserSummary.from_dict(cast(Dict[str, Any], _owner))

            return owner

        owner = _parse_owner(d.pop("owner", UNSET))

        project = Project(
            id=id,
            name=name,
            owner=owner,
        )

        return project
