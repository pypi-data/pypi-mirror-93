from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.boxes_paginated_list import BoxesPaginatedList
from ...models.list_boxes_sort import ListBoxesSort
from ...models.schema_fields_query_param import SchemaFieldsQueryParam
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListBoxesSort] = ListBoxesSort.MODIFIEDATDESC,
    schema_id: Union[Unset, str] = UNSET,
    schema_fields: Union[SchemaFieldsQueryParam, Unset] = UNSET,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    empty_positions: Union[Unset, int] = UNSET,
    empty_positionsgte: Union[Unset, int] = UNSET,
    empty_positionsgt: Union[Unset, int] = UNSET,
    empty_positionslte: Union[Unset, int] = UNSET,
    empty_positionslt: Union[Unset, int] = UNSET,
    empty_containers: Union[Unset, int] = UNSET,
    empty_containersgte: Union[Unset, int] = UNSET,
    empty_containersgt: Union[Unset, int] = UNSET,
    empty_containerslte: Union[Unset, int] = UNSET,
    empty_containerslt: Union[Unset, int] = UNSET,
    ancestor_storage_id: Union[Unset, str] = UNSET,
    storage_contents_id: Union[Unset, str] = UNSET,
    storage_contents_ids: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    barcodes: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/boxes".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_sort: Union[Unset, ListBoxesSort] = UNSET
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
    if schema_id is not UNSET:
        params["schemaId"] = schema_id
    if schema_fields is not UNSET:
        params["schemaFields"] = json_schema_fields
    if modified_at is not UNSET:
        params["modifiedAt"] = modified_at
    if name is not UNSET:
        params["name"] = name
    if name_includes is not UNSET:
        params["nameIncludes"] = name_includes
    if empty_positions is not UNSET:
        params["emptyPositions"] = empty_positions
    if empty_positionsgte is not UNSET:
        params["emptyPositions.gte"] = empty_positionsgte
    if empty_positionsgt is not UNSET:
        params["emptyPositions.gt"] = empty_positionsgt
    if empty_positionslte is not UNSET:
        params["emptyPositions.lte"] = empty_positionslte
    if empty_positionslt is not UNSET:
        params["emptyPositions.lt"] = empty_positionslt
    if empty_containers is not UNSET:
        params["emptyContainers"] = empty_containers
    if empty_containersgte is not UNSET:
        params["emptyContainers.gte"] = empty_containersgte
    if empty_containersgt is not UNSET:
        params["emptyContainers.gt"] = empty_containersgt
    if empty_containerslte is not UNSET:
        params["emptyContainers.lte"] = empty_containerslte
    if empty_containerslt is not UNSET:
        params["emptyContainers.lt"] = empty_containerslt
    if ancestor_storage_id is not UNSET:
        params["ancestorStorageId"] = ancestor_storage_id
    if storage_contents_id is not UNSET:
        params["storageContentsId"] = storage_contents_id
    if storage_contents_ids is not UNSET:
        params["storageContentsIds"] = storage_contents_ids
    if archive_reason is not UNSET:
        params["archiveReason"] = archive_reason
    if ids is not UNSET:
        params["ids"] = ids
    if barcodes is not UNSET:
        params["barcodes"] = barcodes

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[BoxesPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = BoxesPaginatedList.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json())

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[BoxesPaginatedList, BadRequestError]]:
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
    sort: Union[Unset, ListBoxesSort] = ListBoxesSort.MODIFIEDATDESC,
    schema_id: Union[Unset, str] = UNSET,
    schema_fields: Union[SchemaFieldsQueryParam, Unset] = UNSET,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    empty_positions: Union[Unset, int] = UNSET,
    empty_positionsgte: Union[Unset, int] = UNSET,
    empty_positionsgt: Union[Unset, int] = UNSET,
    empty_positionslte: Union[Unset, int] = UNSET,
    empty_positionslt: Union[Unset, int] = UNSET,
    empty_containers: Union[Unset, int] = UNSET,
    empty_containersgte: Union[Unset, int] = UNSET,
    empty_containersgt: Union[Unset, int] = UNSET,
    empty_containerslte: Union[Unset, int] = UNSET,
    empty_containerslt: Union[Unset, int] = UNSET,
    ancestor_storage_id: Union[Unset, str] = UNSET,
    storage_contents_id: Union[Unset, str] = UNSET,
    storage_contents_ids: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    barcodes: Union[Unset, str] = UNSET,
) -> Response[Union[BoxesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        schema_id=schema_id,
        schema_fields=schema_fields,
        modified_at=modified_at,
        name=name,
        name_includes=name_includes,
        empty_positions=empty_positions,
        empty_positionsgte=empty_positionsgte,
        empty_positionsgt=empty_positionsgt,
        empty_positionslte=empty_positionslte,
        empty_positionslt=empty_positionslt,
        empty_containers=empty_containers,
        empty_containersgte=empty_containersgte,
        empty_containersgt=empty_containersgt,
        empty_containerslte=empty_containerslte,
        empty_containerslt=empty_containerslt,
        ancestor_storage_id=ancestor_storage_id,
        storage_contents_id=storage_contents_id,
        storage_contents_ids=storage_contents_ids,
        archive_reason=archive_reason,
        ids=ids,
        barcodes=barcodes,
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
    sort: Union[Unset, ListBoxesSort] = ListBoxesSort.MODIFIEDATDESC,
    schema_id: Union[Unset, str] = UNSET,
    schema_fields: Union[SchemaFieldsQueryParam, Unset] = UNSET,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    empty_positions: Union[Unset, int] = UNSET,
    empty_positionsgte: Union[Unset, int] = UNSET,
    empty_positionsgt: Union[Unset, int] = UNSET,
    empty_positionslte: Union[Unset, int] = UNSET,
    empty_positionslt: Union[Unset, int] = UNSET,
    empty_containers: Union[Unset, int] = UNSET,
    empty_containersgte: Union[Unset, int] = UNSET,
    empty_containersgt: Union[Unset, int] = UNSET,
    empty_containerslte: Union[Unset, int] = UNSET,
    empty_containerslt: Union[Unset, int] = UNSET,
    ancestor_storage_id: Union[Unset, str] = UNSET,
    storage_contents_id: Union[Unset, str] = UNSET,
    storage_contents_ids: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    barcodes: Union[Unset, str] = UNSET,
) -> Optional[Union[BoxesPaginatedList, BadRequestError]]:
    """ List boxes """

    return sync_detailed(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        schema_id=schema_id,
        schema_fields=schema_fields,
        modified_at=modified_at,
        name=name,
        name_includes=name_includes,
        empty_positions=empty_positions,
        empty_positionsgte=empty_positionsgte,
        empty_positionsgt=empty_positionsgt,
        empty_positionslte=empty_positionslte,
        empty_positionslt=empty_positionslt,
        empty_containers=empty_containers,
        empty_containersgte=empty_containersgte,
        empty_containersgt=empty_containersgt,
        empty_containerslte=empty_containerslte,
        empty_containerslt=empty_containerslt,
        ancestor_storage_id=ancestor_storage_id,
        storage_contents_id=storage_contents_id,
        storage_contents_ids=storage_contents_ids,
        archive_reason=archive_reason,
        ids=ids,
        barcodes=barcodes,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListBoxesSort] = ListBoxesSort.MODIFIEDATDESC,
    schema_id: Union[Unset, str] = UNSET,
    schema_fields: Union[SchemaFieldsQueryParam, Unset] = UNSET,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    empty_positions: Union[Unset, int] = UNSET,
    empty_positionsgte: Union[Unset, int] = UNSET,
    empty_positionsgt: Union[Unset, int] = UNSET,
    empty_positionslte: Union[Unset, int] = UNSET,
    empty_positionslt: Union[Unset, int] = UNSET,
    empty_containers: Union[Unset, int] = UNSET,
    empty_containersgte: Union[Unset, int] = UNSET,
    empty_containersgt: Union[Unset, int] = UNSET,
    empty_containerslte: Union[Unset, int] = UNSET,
    empty_containerslt: Union[Unset, int] = UNSET,
    ancestor_storage_id: Union[Unset, str] = UNSET,
    storage_contents_id: Union[Unset, str] = UNSET,
    storage_contents_ids: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    barcodes: Union[Unset, str] = UNSET,
) -> Response[Union[BoxesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        schema_id=schema_id,
        schema_fields=schema_fields,
        modified_at=modified_at,
        name=name,
        name_includes=name_includes,
        empty_positions=empty_positions,
        empty_positionsgte=empty_positionsgte,
        empty_positionsgt=empty_positionsgt,
        empty_positionslte=empty_positionslte,
        empty_positionslt=empty_positionslt,
        empty_containers=empty_containers,
        empty_containersgte=empty_containersgte,
        empty_containersgt=empty_containersgt,
        empty_containerslte=empty_containerslte,
        empty_containerslt=empty_containerslt,
        ancestor_storage_id=ancestor_storage_id,
        storage_contents_id=storage_contents_id,
        storage_contents_ids=storage_contents_ids,
        archive_reason=archive_reason,
        ids=ids,
        barcodes=barcodes,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListBoxesSort] = ListBoxesSort.MODIFIEDATDESC,
    schema_id: Union[Unset, str] = UNSET,
    schema_fields: Union[SchemaFieldsQueryParam, Unset] = UNSET,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    empty_positions: Union[Unset, int] = UNSET,
    empty_positionsgte: Union[Unset, int] = UNSET,
    empty_positionsgt: Union[Unset, int] = UNSET,
    empty_positionslte: Union[Unset, int] = UNSET,
    empty_positionslt: Union[Unset, int] = UNSET,
    empty_containers: Union[Unset, int] = UNSET,
    empty_containersgte: Union[Unset, int] = UNSET,
    empty_containersgt: Union[Unset, int] = UNSET,
    empty_containerslte: Union[Unset, int] = UNSET,
    empty_containerslt: Union[Unset, int] = UNSET,
    ancestor_storage_id: Union[Unset, str] = UNSET,
    storage_contents_id: Union[Unset, str] = UNSET,
    storage_contents_ids: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    barcodes: Union[Unset, str] = UNSET,
) -> Optional[Union[BoxesPaginatedList, BadRequestError]]:
    """ List boxes """

    return (
        await asyncio_detailed(
            client=client,
            page_size=page_size,
            next_token=next_token,
            sort=sort,
            schema_id=schema_id,
            schema_fields=schema_fields,
            modified_at=modified_at,
            name=name,
            name_includes=name_includes,
            empty_positions=empty_positions,
            empty_positionsgte=empty_positionsgte,
            empty_positionsgt=empty_positionsgt,
            empty_positionslte=empty_positionslte,
            empty_positionslt=empty_positionslt,
            empty_containers=empty_containers,
            empty_containersgte=empty_containersgte,
            empty_containersgt=empty_containersgt,
            empty_containerslte=empty_containerslte,
            empty_containerslt=empty_containerslt,
            ancestor_storage_id=ancestor_storage_id,
            storage_contents_id=storage_contents_id,
            storage_contents_ids=storage_contents_ids,
            archive_reason=archive_reason,
            ids=ids,
            barcodes=barcodes,
        )
    ).parsed
