from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.containers_paginated_list import ContainersPaginatedList
from ...models.list_containers_checkout_status import ListContainersCheckoutStatus
from ...models.list_containers_sort import ListContainersSort
from ...models.schema_fields_query_param import SchemaFieldsQueryParam
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListContainersSort] = ListContainersSort.MODIFIEDAT,
    schema_id: Union[Unset, str] = UNSET,
    schema_fields: Union[SchemaFieldsQueryParam, Unset] = UNSET,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    ancestor_storage_id: Union[Unset, str] = UNSET,
    storage_contents_id: Union[Unset, str] = UNSET,
    storage_contents_ids: Union[Unset, List[str]] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    parent_storage_schema_id: Union[Unset, str] = UNSET,
    assay_run_id: Union[Unset, str] = UNSET,
    checkout_status: Union[Unset, ListContainersCheckoutStatus] = UNSET,
    ids: Union[Unset, str] = UNSET,
    barcodes: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/containers".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_sort: Union[Unset, ListContainersSort] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort

    json_schema_fields: Union[Unset, Dict[str, Any]] = UNSET
    if not isinstance(schema_fields, Unset):
        json_schema_fields = schema_fields.to_dict()

    json_storage_contents_ids: Union[Unset, List[Any]] = UNSET
    if not isinstance(storage_contents_ids, Unset):
        json_storage_contents_ids = storage_contents_ids

    json_checkout_status: Union[Unset, ListContainersCheckoutStatus] = UNSET
    if not isinstance(checkout_status, Unset):
        json_checkout_status = checkout_status

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
    if ancestor_storage_id is not UNSET:
        params["ancestorStorageId"] = ancestor_storage_id
    if storage_contents_id is not UNSET:
        params["storageContentsId"] = storage_contents_id
    if storage_contents_ids is not UNSET:
        params["storageContentsIds"] = json_storage_contents_ids
    if archive_reason is not UNSET:
        params["archiveReason"] = archive_reason
    if parent_storage_schema_id is not UNSET:
        params["parentStorageSchemaId"] = parent_storage_schema_id
    if assay_run_id is not UNSET:
        params["assayRunId"] = assay_run_id
    if checkout_status is not UNSET:
        params["checkoutStatus"] = json_checkout_status
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[ContainersPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = ContainersPaginatedList.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json())

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ContainersPaginatedList, BadRequestError]]:
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
    sort: Union[Unset, ListContainersSort] = ListContainersSort.MODIFIEDAT,
    schema_id: Union[Unset, str] = UNSET,
    schema_fields: Union[SchemaFieldsQueryParam, Unset] = UNSET,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    ancestor_storage_id: Union[Unset, str] = UNSET,
    storage_contents_id: Union[Unset, str] = UNSET,
    storage_contents_ids: Union[Unset, List[str]] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    parent_storage_schema_id: Union[Unset, str] = UNSET,
    assay_run_id: Union[Unset, str] = UNSET,
    checkout_status: Union[Unset, ListContainersCheckoutStatus] = UNSET,
    ids: Union[Unset, str] = UNSET,
    barcodes: Union[Unset, str] = UNSET,
) -> Response[Union[ContainersPaginatedList, BadRequestError]]:
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
        ancestor_storage_id=ancestor_storage_id,
        storage_contents_id=storage_contents_id,
        storage_contents_ids=storage_contents_ids,
        archive_reason=archive_reason,
        parent_storage_schema_id=parent_storage_schema_id,
        assay_run_id=assay_run_id,
        checkout_status=checkout_status,
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
    sort: Union[Unset, ListContainersSort] = ListContainersSort.MODIFIEDAT,
    schema_id: Union[Unset, str] = UNSET,
    schema_fields: Union[SchemaFieldsQueryParam, Unset] = UNSET,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    ancestor_storage_id: Union[Unset, str] = UNSET,
    storage_contents_id: Union[Unset, str] = UNSET,
    storage_contents_ids: Union[Unset, List[str]] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    parent_storage_schema_id: Union[Unset, str] = UNSET,
    assay_run_id: Union[Unset, str] = UNSET,
    checkout_status: Union[Unset, ListContainersCheckoutStatus] = UNSET,
    ids: Union[Unset, str] = UNSET,
    barcodes: Union[Unset, str] = UNSET,
) -> Optional[Union[ContainersPaginatedList, BadRequestError]]:
    """ List containers """

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
        ancestor_storage_id=ancestor_storage_id,
        storage_contents_id=storage_contents_id,
        storage_contents_ids=storage_contents_ids,
        archive_reason=archive_reason,
        parent_storage_schema_id=parent_storage_schema_id,
        assay_run_id=assay_run_id,
        checkout_status=checkout_status,
        ids=ids,
        barcodes=barcodes,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListContainersSort] = ListContainersSort.MODIFIEDAT,
    schema_id: Union[Unset, str] = UNSET,
    schema_fields: Union[SchemaFieldsQueryParam, Unset] = UNSET,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    ancestor_storage_id: Union[Unset, str] = UNSET,
    storage_contents_id: Union[Unset, str] = UNSET,
    storage_contents_ids: Union[Unset, List[str]] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    parent_storage_schema_id: Union[Unset, str] = UNSET,
    assay_run_id: Union[Unset, str] = UNSET,
    checkout_status: Union[Unset, ListContainersCheckoutStatus] = UNSET,
    ids: Union[Unset, str] = UNSET,
    barcodes: Union[Unset, str] = UNSET,
) -> Response[Union[ContainersPaginatedList, BadRequestError]]:
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
        ancestor_storage_id=ancestor_storage_id,
        storage_contents_id=storage_contents_id,
        storage_contents_ids=storage_contents_ids,
        archive_reason=archive_reason,
        parent_storage_schema_id=parent_storage_schema_id,
        assay_run_id=assay_run_id,
        checkout_status=checkout_status,
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
    sort: Union[Unset, ListContainersSort] = ListContainersSort.MODIFIEDAT,
    schema_id: Union[Unset, str] = UNSET,
    schema_fields: Union[SchemaFieldsQueryParam, Unset] = UNSET,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    ancestor_storage_id: Union[Unset, str] = UNSET,
    storage_contents_id: Union[Unset, str] = UNSET,
    storage_contents_ids: Union[Unset, List[str]] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    parent_storage_schema_id: Union[Unset, str] = UNSET,
    assay_run_id: Union[Unset, str] = UNSET,
    checkout_status: Union[Unset, ListContainersCheckoutStatus] = UNSET,
    ids: Union[Unset, str] = UNSET,
    barcodes: Union[Unset, str] = UNSET,
) -> Optional[Union[ContainersPaginatedList, BadRequestError]]:
    """ List containers """

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
            ancestor_storage_id=ancestor_storage_id,
            storage_contents_id=storage_contents_id,
            storage_contents_ids=storage_contents_ids,
            archive_reason=archive_reason,
            parent_storage_schema_id=parent_storage_schema_id,
            assay_run_id=assay_run_id,
            checkout_status=checkout_status,
            ids=ids,
            barcodes=barcodes,
        )
    ).parsed
