import datetime
from typing import Any, Dict, List, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.fields import Fields
from ..models.request_assignees_item import RequestAssigneesItem
from ..models.request_status import RequestStatus
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class Request:
    """  """

    id: str
    created_at: datetime.datetime
    fields: Fields
    display_id: str
    assignees: List[Union[RequestAssigneesItem, RequestAssigneesItem]]
    request_status: RequestStatus
    web_url: str
    scheduled_on: Union[Unset, datetime.date] = UNSET
    project_id: Union[Unset, str] = UNSET
    api_url: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        created_at = self.created_at.isoformat()

        fields = self.fields.to_dict()

        display_id = self.display_id
        assignees = []
        for assignees_item_data in self.assignees:
            if isinstance(assignees_item_data, RequestAssigneesItem):
                assignees_item = assignees_item_data.to_dict()

            else:
                assignees_item = assignees_item_data.to_dict()

            assignees.append(assignees_item)

        request_status = self.request_status.value

        web_url = self.web_url
        scheduled_on: Union[Unset, str] = UNSET
        if not isinstance(self.scheduled_on, Unset):
            scheduled_on = self.scheduled_on.isoformat()

        project_id = self.project_id
        api_url = self.api_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "createdAt": created_at,
                "fields": fields,
                "displayId": display_id,
                "assignees": assignees,
                "requestStatus": request_status,
                "webURL": web_url,
            }
        )
        if scheduled_on is not UNSET:
            field_dict["scheduledOn"] = scheduled_on
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if api_url is not UNSET:
            field_dict["apiURL"] = api_url

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "Request":
        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("createdAt"))

        fields = Fields.from_dict(d.pop("fields"))

        display_id = d.pop("displayId")

        assignees = []
        _assignees = d.pop("assignees")
        for assignees_item_data in _assignees:

            def _parse_assignees_item(data: Any) -> Union[RequestAssigneesItem, RequestAssigneesItem]:
                data = None if isinstance(data, Unset) else data
                assignees_item: Union[RequestAssigneesItem, RequestAssigneesItem]
                try:
                    assignees_item = RequestAssigneesItem.from_dict(data)

                    return assignees_item
                except:  # noqa: E722
                    pass
                assignees_item = RequestAssigneesItem.from_dict(data)

                return assignees_item

            assignees_item = _parse_assignees_item(assignees_item_data)

            assignees.append(assignees_item)

        request_status = RequestStatus(d.pop("requestStatus"))

        web_url = d.pop("webURL")

        scheduled_on = None
        _scheduled_on = d.pop("scheduledOn", UNSET)
        if _scheduled_on is not None:
            scheduled_on = isoparse(cast(str, _scheduled_on)).date()

        project_id = d.pop("projectId", UNSET)

        api_url = d.pop("apiURL", UNSET)

        request = Request(
            id=id,
            created_at=created_at,
            fields=fields,
            display_id=display_id,
            assignees=assignees,
            request_status=request_status,
            web_url=web_url,
            scheduled_on=scheduled_on,
            project_id=project_id,
            api_url=api_url,
        )

        return request
