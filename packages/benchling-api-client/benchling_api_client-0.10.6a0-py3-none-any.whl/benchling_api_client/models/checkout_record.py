from typing import Any, Dict, Optional, Union, cast

import attr

from ..models.checkout_record_status import CheckoutRecordStatus
from ..models.team_summary import TeamSummary
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class CheckoutRecord:
    """  """

    status: CheckoutRecordStatus
    comment: str
    modified_at: str
    assignee: Optional[Union[Unset, UserSummary, TeamSummary]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        comment = self.comment
        modified_at = self.modified_at
        assignee: Optional[Union[Unset, UserSummary, TeamSummary]]
        if isinstance(self.assignee, Unset):
            assignee = UNSET
        elif self.assignee is None:
            assignee: Optional[Union[Unset, UserSummary, TeamSummary]] = None
        elif isinstance(self.assignee, UserSummary):
            assignee = UNSET
            if not isinstance(self.assignee, Unset):
                assignee = self.assignee.to_dict()

        else:
            assignee = UNSET
            if not isinstance(self.assignee, Unset):
                assignee = self.assignee.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "status": status,
                "comment": comment,
                "modifiedAt": modified_at,
            }
        )
        if assignee is not UNSET:
            field_dict["assignee"] = assignee

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "CheckoutRecord":
        d = src_dict.copy()
        status = CheckoutRecordStatus(d.pop("status"))

        comment = d.pop("comment")

        modified_at = d.pop("modifiedAt")

        def _parse_assignee(data: Any) -> Optional[Union[Unset, UserSummary, TeamSummary]]:
            data = None if isinstance(data, Unset) else data
            assignee: Optional[Union[Unset, UserSummary, TeamSummary]]
            try:
                assignee = UNSET
                _assignee = data
                if _assignee is not None and not isinstance(_assignee, Unset):
                    assignee = UserSummary.from_dict(cast(Dict[str, Any], _assignee))

                return assignee
            except:  # noqa: E722
                pass
            assignee = UNSET
            _assignee = data
            if _assignee is not None and not isinstance(_assignee, Unset):
                assignee = TeamSummary.from_dict(cast(Dict[str, Any], _assignee))

            return assignee

        assignee = _parse_assignee(d.pop("assignee", UNSET))

        checkout_record = CheckoutRecord(
            status=status,
            comment=comment,
            modified_at=modified_at,
            assignee=assignee,
        )

        return checkout_record
