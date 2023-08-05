import datetime
from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.assay_results_paginated_list import AssayResultsPaginatedList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    schema_id: str,
    min_created_time: Union[Unset, datetime.datetime] = UNSET,
    max_created_time: Union[Unset, datetime.datetime] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    entity_ids: Union[Unset, str] = UNSET,
    assay_run_ids: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/assay-results".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_min_created_time: Union[Unset, str] = UNSET
    if not isinstance(min_created_time, Unset):
        json_min_created_time = min_created_time.isoformat()

    json_max_created_time: Union[Unset, str] = UNSET
    if not isinstance(max_created_time, Unset):
        json_max_created_time = max_created_time.isoformat()

    params: Dict[str, Any] = {
        "schemaId": schema_id,
    }
    if min_created_time is not UNSET:
        params["minCreatedTime"] = json_min_created_time
    if max_created_time is not UNSET:
        params["maxCreatedTime"] = json_max_created_time
    if next_token is not UNSET:
        params["nextToken"] = next_token
    if page_size is not UNSET:
        params["pageSize"] = page_size
    if entity_ids is not UNSET:
        params["entityIds"] = entity_ids
    if assay_run_ids is not UNSET:
        params["assayRunIds"] = assay_run_ids
    if ids is not UNSET:
        params["ids"] = ids

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[AssayResultsPaginatedList]:
    if response.status_code == 200:
        response_200 = AssayResultsPaginatedList.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[AssayResultsPaginatedList]:
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
    min_created_time: Union[Unset, datetime.datetime] = UNSET,
    max_created_time: Union[Unset, datetime.datetime] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    entity_ids: Union[Unset, str] = UNSET,
    assay_run_ids: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
) -> Response[AssayResultsPaginatedList]:
    kwargs = _get_kwargs(
        client=client,
        schema_id=schema_id,
        min_created_time=min_created_time,
        max_created_time=max_created_time,
        next_token=next_token,
        page_size=page_size,
        entity_ids=entity_ids,
        assay_run_ids=assay_run_ids,
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
    min_created_time: Union[Unset, datetime.datetime] = UNSET,
    max_created_time: Union[Unset, datetime.datetime] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    entity_ids: Union[Unset, str] = UNSET,
    assay_run_ids: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
) -> Optional[AssayResultsPaginatedList]:
    """  """

    return sync_detailed(
        client=client,
        schema_id=schema_id,
        min_created_time=min_created_time,
        max_created_time=max_created_time,
        next_token=next_token,
        page_size=page_size,
        entity_ids=entity_ids,
        assay_run_ids=assay_run_ids,
        ids=ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    schema_id: str,
    min_created_time: Union[Unset, datetime.datetime] = UNSET,
    max_created_time: Union[Unset, datetime.datetime] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    entity_ids: Union[Unset, str] = UNSET,
    assay_run_ids: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
) -> Response[AssayResultsPaginatedList]:
    kwargs = _get_kwargs(
        client=client,
        schema_id=schema_id,
        min_created_time=min_created_time,
        max_created_time=max_created_time,
        next_token=next_token,
        page_size=page_size,
        entity_ids=entity_ids,
        assay_run_ids=assay_run_ids,
        ids=ids,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    schema_id: str,
    min_created_time: Union[Unset, datetime.datetime] = UNSET,
    max_created_time: Union[Unset, datetime.datetime] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    entity_ids: Union[Unset, str] = UNSET,
    assay_run_ids: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
) -> Optional[AssayResultsPaginatedList]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            schema_id=schema_id,
            min_created_time=min_created_time,
            max_created_time=max_created_time,
            next_token=next_token,
            page_size=page_size,
            entity_ids=entity_ids,
            assay_run_ids=assay_run_ids,
            ids=ids,
        )
    ).parsed
