from typing import Any, Dict, Union, cast

import attr

from ..models.default_concentration_summary import DefaultConcentrationSummary
from ..models.fields import Fields
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class BatchUpdate:
    """  """

    default_concentration: Union[DefaultConcentrationSummary, Unset] = UNSET
    fields: Union[Fields, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        default_concentration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.default_concentration, Unset):
            default_concentration = self.default_concentration.to_dict()

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if default_concentration is not UNSET:
            field_dict["defaultConcentration"] = default_concentration
        if fields is not UNSET:
            field_dict["fields"] = fields

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "BatchUpdate":
        d = src_dict.copy()
        default_concentration: Union[DefaultConcentrationSummary, Unset] = UNSET
        _default_concentration = d.pop("defaultConcentration", UNSET)
        if _default_concentration is not None and not isinstance(_default_concentration, Unset):
            default_concentration = DefaultConcentrationSummary.from_dict(cast(Dict[str, Any], _default_concentration))

        fields: Union[Fields, Unset] = UNSET
        _fields = d.pop("fields", UNSET)
        if _fields is not None and not isinstance(_fields, Unset):
            fields = Fields.from_dict(cast(Dict[str, Any], _fields))

        batch_update = BatchUpdate(
            default_concentration=default_concentration,
            fields=fields,
        )

        return batch_update
