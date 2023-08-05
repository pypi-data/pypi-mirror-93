from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class BadRequestError:
    """  """

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update({})

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "BadRequestError":
        src_dict.copy()
        bad_request_error = BadRequestError()

        return bad_request_error
