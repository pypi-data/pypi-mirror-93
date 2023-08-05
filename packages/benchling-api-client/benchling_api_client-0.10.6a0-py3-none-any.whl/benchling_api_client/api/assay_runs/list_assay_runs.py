from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.assay_runs_paginated_list import AssayRunsPaginatedList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    schema_id: str,
    min_created_time: Union[Unset, int] = UNSET,
    max_created_time: Union[Unset, int] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    ids: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/assay-runs".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    params: Dict[str, Any] = {
        "schemaId": schema_id,
    }
    if min_created_time is not UNSET:
        params["minCreatedTime"] = min_created_time
    if max_created_time is not UNSET:
        params["maxCreatedTime"] = max_created_time
    if next_token is not UNSET:
        params["nextToken"] = next_token
    if page_size is not UNSET:
        params["pageSize"] = page_size
    if ids is not UNSET:
        params["ids"] = ids

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[AssayRunsPaginatedList]:
    if response.status_code == 200:
        response_200 = AssayRunsPaginatedList.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[AssayRunsPaginatedList]:
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
    min_created_time: Union[Unset, int] = UNSET,
    max_created_time: Union[Unset, int] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    ids: Union[Unset, str] = UNSET,
) -> Response[AssayRunsPaginatedList]:
    kwargs = _get_kwargs(
        client=client,
        schema_id=schema_id,
        min_created_time=min_created_time,
        max_created_time=max_created_time,
        next_token=next_token,
        page_size=page_size,
        ids=ids,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    schema_id: str,
    min_created_time: Union[Unset, int] = UNSET,
    max_created_time: Union[Unset, int] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    ids: Union[Unset, str] = UNSET,
) -> Optional[AssayRunsPaginatedList]:
    """  """

    return sync_detailed(
        client=client,
        schema_id=schema_id,
        min_created_time=min_created_time,
        max_created_time=max_created_time,
        next_token=next_token,
        page_size=page_size,
        ids=ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    schema_id: str,
    min_created_time: Union[Unset, int] = UNSET,
    max_created_time: Union[Unset, int] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    ids: Union[Unset, str] = UNSET,
) -> Response[AssayRunsPaginatedList]:
    kwargs = _get_kwargs(
        client=client,
        schema_id=schema_id,
        min_created_time=min_created_time,
        max_created_time=max_created_time,
        next_token=next_token,
        page_size=page_size,
        ids=ids,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    schema_id: str,
    min_created_time: Union[Unset, int] = UNSET,
    max_created_time: Union[Unset, int] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    ids: Union[Unset, str] = UNSET,
) -> Optional[AssayRunsPaginatedList]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            schema_id=schema_id,
            min_created_time=min_created_time,
            max_created_time=max_created_time,
            next_token=next_token,
            page_size=page_size,
            ids=ids,
        )
    ).parsed
