from typing import Any, Dict, List, Union

import attr

from ..models.request_response_samples_item_status import RequestResponseSamplesItemStatus
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class RequestResponseSamplesItem:
    """  """

    status: Union[Unset, RequestResponseSamplesItemStatus] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status: Union[Unset, RequestResponseSamplesItemStatus] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "RequestResponseSamplesItem":
        d = src_dict.copy()
        status = None
        _status = d.pop("status", UNSET)
        if _status is not None:
            status = RequestResponseSamplesItemStatus(_status)

        request_response_samples_item = RequestResponseSamplesItem(
            status=status,
        )

        request_response_samples_item.additional_properties = d
        return request_response_samples_item

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
