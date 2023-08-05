from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.batches_paginated_list import BatchesPaginatedList
from ...models.list_batches_sort import ListBatchesSort
from ...models.schema_fields_query_param import SchemaFieldsQueryParam
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListBatchesSort] = ListBatchesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, str] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    schema_fields: Union[SchemaFieldsQueryParam, Unset] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/batches".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_sort: Union[Unset, ListBatchesSort] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort

    json_schema_fields: Union[Unset, Dict[str, Any]] = UNSET
    if not isinstance(schema_fields, Unset):
        json_schema_fields = schema_fields.to_dict()

    params: Dict[str, Any] = {}
    if page_size is not UNSET:
        params["pageSize"] = page_size
    if next_token is not UNSET:
        params["nextToken"] = next_token
    if sort is not UNSET:
        params["sort"] = json_sort
    if modified_at is not UNSET:
        params["modifiedAt"] = modified_at
    if schema_id is not UNSET:
        params["schemaId"] = schema_id
    if schema_fields is not UNSET:
        params["schemaFields"] = json_schema_fields
    if archive_reason is not UNSET:
        params["archiveReason"] = archive_reason
    if ids is not UNSET:
        params["ids"] = ids

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[BatchesPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = BatchesPaginatedList.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json())

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[BatchesPaginatedList, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListBatchesSort] = ListBatchesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, str] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    schema_fields: Union[SchemaFieldsQueryParam, Unset] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
) -> Response[Union[BatchesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        schema_id=schema_id,
        schema_fields=schema_fields,
        archive_reason=archive_reason,
        ids=ids,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListBatchesSort] = ListBatchesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, str] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    schema_fields: Union[SchemaFieldsQueryParam, Unset] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
) -> Optional[Union[BatchesPaginatedList, BadRequestError]]:
    """ List batches """

    return sync_detailed(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        schema_id=schema_id,
        schema_fields=schema_fields,
        archive_reason=archive_reason,
        ids=ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListBatchesSort] = ListBatchesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, str] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    schema_fields: Union[SchemaFieldsQueryParam, Unset] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
) -> Response[Union[BatchesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        schema_id=schema_id,
        schema_fields=schema_fields,
        archive_reason=archive_reason,
        ids=ids,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListBatchesSort] = ListBatchesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, str] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    schema_fields: Union[SchemaFieldsQueryParam, Unset] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
) -> Optional[Union[BatchesPaginatedList, BadRequestError]]:
    """ List batches """

    return (
        await asyncio_detailed(
            client=client,
            page_size=page_size,
            next_token=next_token,
            sort=sort,
            modified_at=modified_at,
            schema_id=schema_id,
            schema_fields=schema_fields,
            archive_reason=archive_reason,
            ids=ids,
        )
    ).parsed
