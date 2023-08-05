from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.entries_paginated_list import EntriesPaginatedList
from ...models.list_entries_review_status import ListEntriesReviewStatus
from ...models.list_entries_sort import ListEntriesSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListEntriesSort] = ListEntriesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    review_status: Union[Unset, ListEntriesReviewStatus] = UNSET,
    mentioned_in: Union[Unset, str] = UNSET,
    mentions: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/entries".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_sort: Union[Unset, ListEntriesSort] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort

    json_review_status: Union[Unset, ListEntriesReviewStatus] = UNSET
    if not isinstance(review_status, Unset):
        json_review_status = review_status

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
    if project_id is not UNSET:
        params["projectId"] = project_id
    if archive_reason is not UNSET:
        params["archiveReason"] = archive_reason
    if review_status is not UNSET:
        params["reviewStatus"] = json_review_status
    if mentioned_in is not UNSET:
        params["mentionedIn"] = mentioned_in
    if mentions is not UNSET:
        params["mentions"] = mentions
    if ids is not UNSET:
        params["ids"] = ids

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[EntriesPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = EntriesPaginatedList.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json())

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[EntriesPaginatedList, BadRequestError]]:
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
    sort: Union[Unset, ListEntriesSort] = ListEntriesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    review_status: Union[Unset, ListEntriesReviewStatus] = UNSET,
    mentioned_in: Union[Unset, str] = UNSET,
    mentions: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
) -> Response[Union[EntriesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        project_id=project_id,
        archive_reason=archive_reason,
        review_status=review_status,
        mentioned_in=mentioned_in,
        mentions=mentions,
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
    sort: Union[Unset, ListEntriesSort] = ListEntriesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    review_status: Union[Unset, ListEntriesReviewStatus] = UNSET,
    mentioned_in: Union[Unset, str] = UNSET,
    mentions: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
) -> Optional[Union[EntriesPaginatedList, BadRequestError]]:
    """ List notebook entries """

    return sync_detailed(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        project_id=project_id,
        archive_reason=archive_reason,
        review_status=review_status,
        mentioned_in=mentioned_in,
        mentions=mentions,
        ids=ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListEntriesSort] = ListEntriesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    review_status: Union[Unset, ListEntriesReviewStatus] = UNSET,
    mentioned_in: Union[Unset, str] = UNSET,
    mentions: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
) -> Response[Union[EntriesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        project_id=project_id,
        archive_reason=archive_reason,
        review_status=review_status,
        mentioned_in=mentioned_in,
        mentions=mentions,
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
    sort: Union[Unset, ListEntriesSort] = ListEntriesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    review_status: Union[Unset, ListEntriesReviewStatus] = UNSET,
    mentioned_in: Union[Unset, str] = UNSET,
    mentions: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
) -> Optional[Union[EntriesPaginatedList, BadRequestError]]:
    """ List notebook entries """

    return (
        await asyncio_detailed(
            client=client,
            page_size=page_size,
            next_token=next_token,
            sort=sort,
            modified_at=modified_at,
            name=name,
            project_id=project_id,
            archive_reason=archive_reason,
            review_status=review_status,
            mentioned_in=mentioned_in,
            mentions=mentions,
            ids=ids,
        )
    ).parsed
