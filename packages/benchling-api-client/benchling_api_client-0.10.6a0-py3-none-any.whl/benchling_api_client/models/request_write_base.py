import datetime
from typing import Any, Dict, List, Optional, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.fields import Fields
from ..models.request_write_base_assignees_item import RequestWriteBaseAssigneesItem
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class RequestWriteBase:
    """  """

    assignees: Union[Unset, List[Union[RequestWriteBaseAssigneesItem, RequestWriteBaseAssigneesItem]]] = UNSET
    requestor_id: Union[Unset, Optional[str]] = UNSET
    scheduled_on: Union[Unset, datetime.date] = UNSET
    project_id: Union[Unset, str] = UNSET
    fields: Union[Fields, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        assignees: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.assignees, Unset):
            assignees = []
            for assignees_item_data in self.assignees:
                if isinstance(assignees_item_data, RequestWriteBaseAssigneesItem):
                    assignees_item = assignees_item_data.to_dict()

                else:
                    assignees_item = assignees_item_data.to_dict()

                assignees.append(assignees_item)

        requestor_id = self.requestor_id
        scheduled_on: Union[Unset, str] = UNSET
        if not isinstance(self.scheduled_on, Unset):
            scheduled_on = self.scheduled_on.isoformat()

        project_id = self.project_id
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if assignees is not UNSET:
            field_dict["assignees"] = assignees
        if requestor_id is not UNSET:
            field_dict["requestorId"] = requestor_id
        if scheduled_on is not UNSET:
            field_dict["scheduledOn"] = scheduled_on
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if fields is not UNSET:
            field_dict["fields"] = fields

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "RequestWriteBase":
        d = src_dict.copy()
        assignees = []
        _assignees = d.pop("assignees", UNSET)
        for assignees_item_data in _assignees or []:

            def _parse_assignees_item(data: Any) -> Union[RequestWriteBaseAssigneesItem, RequestWriteBaseAssigneesItem]:
                data = None if isinstance(data, Unset) else data
                assignees_item: Union[RequestWriteBaseAssigneesItem, RequestWriteBaseAssigneesItem]
                try:
                    assignees_item = RequestWriteBaseAssigneesItem.from_dict(data)

                    return assignees_item
                except:  # noqa: E722
                    pass
                assignees_item = RequestWriteBaseAssigneesItem.from_dict(data)

                return assignees_item

            assignees_item = _parse_assignees_item(assignees_item_data)

            assignees.append(assignees_item)

        requestor_id = d.pop("requestorId", UNSET)

        scheduled_on = None
        _scheduled_on = d.pop("scheduledOn", UNSET)
        if _scheduled_on is not None:
            scheduled_on = isoparse(cast(str, _scheduled_on)).date()

        project_id = d.pop("projectId", UNSET)

        fields: Union[Fields, Unset] = UNSET
        _fields = d.pop("fields", UNSET)
        if _fields is not None and not isinstance(_fields, Unset):
            fields = Fields.from_dict(cast(Dict[str, Any], _fields))

        request_write_base = RequestWriteBase(
            assignees=assignees,
            requestor_id=requestor_id,
            scheduled_on=scheduled_on,
            project_id=project_id,
            fields=fields,
        )

        return request_write_base
