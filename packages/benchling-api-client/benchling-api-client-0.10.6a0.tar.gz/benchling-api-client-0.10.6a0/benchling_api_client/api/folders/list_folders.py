from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.folders_paginated_list import FoldersPaginatedList
from ...models.list_folders_sort import ListFoldersSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    sort: Union[Unset, ListFoldersSort] = ListFoldersSort.NAME,
    archive_reason: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    parent_folder_id: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/folders".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_sort: Union[Unset, ListFoldersSort] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort

    params: Dict[str, Any] = {}
    if next_token is not UNSET:
        params["nextToken"] = next_token
    if page_size is not UNSET:
        params["pageSize"] = page_size
    if sort is not UNSET:
        params["sort"] = json_sort
    if archive_reason is not UNSET:
        params["archiveReason"] = archive_reason
    if name_includes is not UNSET:
        params["nameIncludes"] = name_includes
    if parent_folder_id is not UNSET:
        params["parentFolderId"] = parent_folder_id
    if project_id is not UNSET:
        params["projectId"] = project_id
    if ids is not UNSET:
        params["ids"] = ids

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[FoldersPaginatedList]:
    if response.status_code == 200:
        response_200 = FoldersPaginatedList.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[FoldersPaginatedList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    sort: Union[Unset, ListFoldersSort] = ListFoldersSort.NAME,
    archive_reason: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    parent_folder_id: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
) -> Response[FoldersPaginatedList]:
    kwargs = _get_kwargs(
        client=client,
        next_token=next_token,
        page_size=page_size,
        sort=sort,
        archive_reason=archive_reason,
        name_includes=name_includes,
        parent_folder_id=parent_folder_id,
        project_id=project_id,
        ids=ids,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    sort: Union[Unset, ListFoldersSort] = ListFoldersSort.NAME,
    archive_reason: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    parent_folder_id: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
) -> Optional[FoldersPaginatedList]:
    """  """

    return sync_detailed(
        client=client,
        next_token=next_token,
        page_size=page_size,
        sort=sort,
        archive_reason=archive_reason,
        name_includes=name_includes,
        parent_folder_id=parent_folder_id,
        project_id=project_id,
        ids=ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    sort: Union[Unset, ListFoldersSort] = ListFoldersSort.NAME,
    archive_reason: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    parent_folder_id: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
) -> Response[FoldersPaginatedList]:
    kwargs = _get_kwargs(
        client=client,
        next_token=next_token,
        page_size=page_size,
        sort=sort,
        archive_reason=archive_reason,
        name_includes=name_includes,
        parent_folder_id=parent_folder_id,
        project_id=project_id,
        ids=ids,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    sort: Union[Unset, ListFoldersSort] = ListFoldersSort.NAME,
    archive_reason: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    parent_folder_id: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
) -> Optional[FoldersPaginatedList]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            next_token=next_token,
            page_size=page_size,
            sort=sort,
            archive_reason=archive_reason,
            name_includes=name_includes,
            parent_folder_id=parent_folder_id,
            project_id=project_id,
            ids=ids,
        )
    ).parsed
