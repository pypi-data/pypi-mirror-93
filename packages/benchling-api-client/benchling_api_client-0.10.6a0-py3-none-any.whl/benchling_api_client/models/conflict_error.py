from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class ConflictError:
    """  """

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update({})

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ConflictError":
        src_dict.copy()
        conflict_error = ConflictError()

        return conflict_error
