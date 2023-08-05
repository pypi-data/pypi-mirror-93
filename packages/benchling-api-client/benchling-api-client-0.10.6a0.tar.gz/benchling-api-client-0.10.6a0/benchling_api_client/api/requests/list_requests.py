from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.request_status import RequestStatus
from ...models.requests_paginated_list import RequestsPaginatedList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    schema_id: str,
    request_status: Union[Unset, RequestStatus] = UNSET,
    min_created_time: Union[Unset, int] = UNSET,
    max_created_time: Union[Unset, int] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
) -> Dict[str, Any]:
    url = "{}/requests".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_request_status: Union[Unset, RequestStatus] = UNSET
    if not isinstance(request_status, Unset):
        json_request_status = request_status

    params: Dict[str, Any] = {
        "schemaId": schema_id,
    }
    if request_status is not UNSET:
        params["requestStatus"] = json_request_status
    if min_created_time is not UNSET:
        params["minCreatedTime"] = min_created_time
    if max_created_time is not UNSET:
        params["maxCreatedTime"] = max_created_time
    if next_token is not UNSET:
        params["nextToken"] = next_token
    if page_size is not UNSET:
        params["pageSize"] = page_size

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[RequestsPaginatedList]:
    if response.status_code == 200:
        response_200 = RequestsPaginatedList.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[RequestsPaginatedList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    schema_id: str,
    request_status: Union[Unset, RequestStatus] = UNSET,
    min_created_time: Union[Unset, int] = UNSET,
    max_created_time: Union[Unset, int] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
) -> Response[RequestsPaginatedList]:
    kwargs = _get_kwargs(
        client=client,
        schema_id=schema_id,
        request_status=request_status,
        min_created_time=min_created_time,
        max_created_time=max_created_time,
        next_token=next_token,
        page_size=page_size,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    schema_id: str,
    request_status: Union[Unset, RequestStatus] = UNSET,
    min_created_time: Union[Unset, int] = UNSET,
    max_created_time: Union[Unset, int] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
) -> Optional[RequestsPaginatedList]:
    """ List requests """

    return sync_detailed(
        client=client,
        schema_id=schema_id,
        request_status=request_status,
        min_created_time=min_created_time,
        max_created_time=max_created_time,
        next_token=next_token,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    schema_id: str,
    request_status: Union[Unset, RequestStatus] = UNSET,
    min_created_time: Union[Unset, int] = UNSET,
    max_created_time: Union[Unset, int] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
) -> Response[RequestsPaginatedList]:
    kwargs = _get_kwargs(
        client=client,
        schema_id=schema_id,
        request_status=request_status,
        min_created_time=min_created_time,
        max_created_time=max_created_time,
        next_token=next_token,
        page_size=page_size,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    schema_id: str,
    request_status: Union[Unset, RequestStatus] = UNSET,
    min_created_time: Union[Unset, int] = UNSET,
    max_created_time: Union[Unset, int] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
) -> Optional[RequestsPaginatedList]:
    """ List requests """

    return (
        await asyncio_detailed(
            client=client,
            schema_id=schema_id,
            request_status=request_status,
            min_created_time=min_created_time,
            max_created_time=max_created_time,
            next_token=next_token,
            page_size=page_size,
        )
    ).parsed
