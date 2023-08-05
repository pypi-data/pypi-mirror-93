from typing import Any, Dict, Union, cast

import attr

from ..models.async_task_errors import AsyncTaskErrors
from ..models.async_task_response import AsyncTaskResponse
from ..models.async_task_status import AsyncTaskStatus
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class AsyncTask:
    """  """

    status: AsyncTaskStatus
    response: Union[AsyncTaskResponse, Unset] = UNSET
    message: Union[Unset, str] = UNSET
    errors: Union[AsyncTaskErrors, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        response: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.response, Unset):
            response = self.response.to_dict()

        message = self.message
        errors: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = self.errors.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "status": status,
            }
        )
        if response is not UNSET:
            field_dict["response"] = response
        if message is not UNSET:
            field_dict["message"] = message
        if errors is not UNSET:
            field_dict["errors"] = errors

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "AsyncTask":
        d = src_dict.copy()
        status = AsyncTaskStatus(d.pop("status"))

        response: Union[AsyncTaskResponse, Unset] = UNSET
        _response = d.pop("response", UNSET)
        if _response is not None and not isinstance(_response, Unset):
            response = AsyncTaskResponse.from_dict(cast(Dict[str, Any], _response))

        message = d.pop("message", UNSET)

        errors: Union[AsyncTaskErrors, Unset] = UNSET
        _errors = d.pop("errors", UNSET)
        if _errors is not None and not isinstance(_errors, Unset):
            errors = AsyncTaskErrors.from_dict(cast(Dict[str, Any], _errors))

        async_task = AsyncTask(
            status=status,
            response=response,
            message=message,
            errors=errors,
        )

        return async_task
