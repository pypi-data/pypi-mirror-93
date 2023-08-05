from typing import Any, Dict, Union, cast

import attr

from ..models.fields import Fields
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class AssayRunUpdate:
    """  """

    fields: Union[Fields, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if fields is not UNSET:
            field_dict["fields"] = fields

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "AssayRunUpdate":
        d = src_dict.copy()
        fields: Union[Fields, Unset] = UNSET
        _fields = d.pop("fields", UNSET)
        if _fields is not None and not isinstance(_fields, Unset):
            fields = Fields.from_dict(cast(Dict[str, Any], _fields))

        assay_run_update = AssayRunUpdate(
            fields=fields,
        )

        return assay_run_update
