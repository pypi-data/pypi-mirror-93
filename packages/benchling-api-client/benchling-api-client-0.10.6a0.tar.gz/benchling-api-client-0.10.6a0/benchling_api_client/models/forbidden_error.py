from typing import Any, Dict, Union, cast

import attr

from ..models.forbidden_error_error import ForbiddenErrorError
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class ForbiddenError:
    """  """

    error: Union[ForbiddenErrorError, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        error: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ForbiddenError":
        d = src_dict.copy()
        error: Union[ForbiddenErrorError, Unset] = UNSET
        _error = d.pop("error", UNSET)
        if _error is not None and not isinstance(_error, Unset):
            error = ForbiddenErrorError.from_dict(cast(Dict[str, Any], _error))

        forbidden_error = ForbiddenError(
            error=error,
        )

        return forbidden_error
