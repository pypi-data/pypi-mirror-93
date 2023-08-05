from typing import Any, Dict, List, Union

import attr

from ..models.dropdown_option import DropdownOption
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class Dropdown:
    """  """

    name: str
    id: str
    options: Union[Unset, List[DropdownOption]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id
        options: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = []
            for options_item_data in self.options:
                options_item = options_item_data.to_dict()

                options.append(options_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "id": id,
            }
        )
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "Dropdown":
        d = src_dict.copy()
        name = d.pop("name")

        id = d.pop("id")

        options = []
        _options = d.pop("options", UNSET)
        for options_item_data in _options or []:
            options_item = DropdownOption.from_dict(options_item_data)

            options.append(options_item)

        dropdown = Dropdown(
            name=name,
            id=id,
            options=options,
        )

        return dropdown
