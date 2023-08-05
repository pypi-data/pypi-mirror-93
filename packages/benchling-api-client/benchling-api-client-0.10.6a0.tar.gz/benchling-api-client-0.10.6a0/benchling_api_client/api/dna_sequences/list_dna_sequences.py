from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.dna_sequences_paginated_list import DnaSequencesPaginatedList
from ...models.list_dna_sequences_sort import ListDNASequencesSort
from ...models.schema_fields_query_param import SchemaFieldsQueryParam
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListDNASequencesSort] = ListDNASequencesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    bases: Union[Unset, str] = UNSET,
    folder_id: Union[Unset, str] = UNSET,
    mentioned_in: Union[Unset, List[str]] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    registry_id: Union[Unset, Optional[str]] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    schema_fields: Union[SchemaFieldsQueryParam, Unset] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    mentions: Union[Unset, List[str]] = UNSET,
    ids: Union[Unset, str] = UNSET,
    entity_registry_idsany_of: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/dna-sequences".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_sort: Union[Unset, ListDNASequencesSort] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort

    json_mentioned_in: Union[Unset, List[Any]] = UNSET
    if not isinstance(mentioned_in, Unset):
        json_mentioned_in = mentioned_in

    json_schema_fields: Union[Unset, Dict[str, Any]] = UNSET
    if not isinstance(schema_fields, Unset):
        json_schema_fields = schema_fields.to_dict()

    json_mentions: Union[Unset, List[Any]] = UNSET
    if not isinstance(mentions, Unset):
        json_mentions = mentions

    params: Dict[str, Any] = {}
    if page_size is not UNSET:
        params["pageSize"] = page_size
    if next_token is not UNSET:
        params["nextToken"] = next_token
    if sort is not UNSET:
        params["sort"] = json_sort
    if modified_at is not UNSET:
        params["modifiedAt"] = modified_at
    if name is not UNSET:
        params["name"] = name
    if bases is not UNSET:
        params["bases"] = bases
    if folder_id is not UNSET:
        params["folderId"] = folder_id
    if mentioned_in is not UNSET:
        params["mentionedIn"] = json_mentioned_in
    if project_id is not UNSET:
        params["projectId"] = project_id
    if registry_id is not UNSET:
        params["registryId"] = registry_id
    if schema_id is not UNSET:
        params["schemaId"] = schema_id
    if schema_fields is not UNSET:
        params["schemaFields"] = json_schema_fields
    if archive_reason is not UNSET:
        params["archiveReason"] = archive_reason
    if mentions is not UNSET:
        params["mentions"] = json_mentions
    if ids is not UNSET:
        params["ids"] = ids
    if entity_registry_idsany_of is not UNSET:
        params["entityRegistryIds.anyOf"] = entity_registry_idsany_of

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[DnaSequencesPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = DnaSequencesPaginatedList.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json())

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[DnaSequencesPaginatedList, BadRequestError]]:
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
    sort: Union[Unset, ListDNASequencesSort] = ListDNASequencesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    bases: Union[Unset, str] = UNSET,
    folder_id: Union[Unset, str] = UNSET,
    mentioned_in: Union[Unset, List[str]] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    registry_id: Union[Unset, Optional[str]] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    schema_fields: Union[SchemaFieldsQueryParam, Unset] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    mentions: Union[Unset, List[str]] = UNSET,
    ids: Union[Unset, str] = UNSET,
    entity_registry_idsany_of: Union[Unset, str] = UNSET,
) -> Response[Union[DnaSequencesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        bases=bases,
        folder_id=folder_id,
        mentioned_in=mentioned_in,
        project_id=project_id,
        registry_id=registry_id,
        schema_id=schema_id,
        schema_fields=schema_fields,
        archive_reason=archive_reason,
        mentions=mentions,
        ids=ids,
        entity_registry_idsany_of=entity_registry_idsany_of,
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
    sort: Union[Unset, ListDNASequencesSort] = ListDNASequencesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    bases: Union[Unset, str] = UNSET,
    folder_id: Union[Unset, str] = UNSET,
    mentioned_in: Union[Unset, List[str]] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    registry_id: Union[Unset, Optional[str]] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    schema_fields: Union[SchemaFieldsQueryParam, Unset] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    mentions: Union[Unset, List[str]] = UNSET,
    ids: Union[Unset, str] = UNSET,
    entity_registry_idsany_of: Union[Unset, str] = UNSET,
) -> Optional[Union[DnaSequencesPaginatedList, BadRequestError]]:
    """ List DNA sequences """

    return sync_detailed(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        bases=bases,
        folder_id=folder_id,
        mentioned_in=mentioned_in,
        project_id=project_id,
        registry_id=registry_id,
        schema_id=schema_id,
        schema_fields=schema_fields,
        archive_reason=archive_reason,
        mentions=mentions,
        ids=ids,
        entity_registry_idsany_of=entity_registry_idsany_of,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListDNASequencesSort] = ListDNASequencesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    bases: Union[Unset, str] = UNSET,
    folder_id: Union[Unset, str] = UNSET,
    mentioned_in: Union[Unset, List[str]] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    registry_id: Union[Unset, Optional[str]] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    schema_fields: Union[SchemaFieldsQueryParam, Unset] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    mentions: Union[Unset, List[str]] = UNSET,
    ids: Union[Unset, str] = UNSET,
    entity_registry_idsany_of: Union[Unset, str] = UNSET,
) -> Response[Union[DnaSequencesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        bases=bases,
        folder_id=folder_id,
        mentioned_in=mentioned_in,
        project_id=project_id,
        registry_id=registry_id,
        schema_id=schema_id,
        schema_fields=schema_fields,
        archive_reason=archive_reason,
        mentions=mentions,
        ids=ids,
        entity_registry_idsany_of=entity_registry_idsany_of,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListDNASequencesSort] = ListDNASequencesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    bases: Union[Unset, str] = UNSET,
    folder_id: Union[Unset, str] = UNSET,
    mentioned_in: Union[Unset, List[str]] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    registry_id: Union[Unset, Optional[str]] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    schema_fields: Union[SchemaFieldsQueryParam, Unset] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    mentions: Union[Unset, List[str]] = UNSET,
    ids: Union[Unset, str] = UNSET,
    entity_registry_idsany_of: Union[Unset, str] = UNSET,
) -> Optional[Union[DnaSequencesPaginatedList, BadRequestError]]:
    """ List DNA sequences """

    return (
        await asyncio_detailed(
            client=client,
            page_size=page_size,
            next_token=next_token,
            sort=sort,
            modified_at=modified_at,
            name=name,
            bases=bases,
            folder_id=folder_id,
            mentioned_in=mentioned_in,
            project_id=project_id,
            registry_id=registry_id,
            schema_id=schema_id,
            schema_fields=schema_fields,
            archive_reason=archive_reason,
            mentions=mentions,
            ids=ids,
            entity_registry_idsany_of=entity_registry_idsany_of,
        )
    ).parsed
