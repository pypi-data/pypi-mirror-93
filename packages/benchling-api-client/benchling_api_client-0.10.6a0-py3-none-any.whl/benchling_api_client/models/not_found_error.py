from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class NotFoundError:
    """  """

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update({})

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "NotFoundError":
        src_dict.copy()
        not_found_error = NotFoundError()

        return not_found_error
