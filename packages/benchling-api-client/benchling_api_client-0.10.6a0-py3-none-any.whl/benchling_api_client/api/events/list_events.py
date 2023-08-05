from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.events_paginated_list import EventsPaginatedList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    starting_after: Union[Unset, str] = UNSET,
    event_types: Union[Unset, str] = UNSET,
    poll: Union[Unset, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/events".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    params: Dict[str, Any] = {}
    if page_size is not UNSET:
        params["pageSize"] = page_size
    if next_token is not UNSET:
        params["nextToken"] = next_token
    if created_atgte is not UNSET:
        params["createdAt.gte"] = created_atgte
    if starting_after is not UNSET:
        params["startingAfter"] = starting_after
    if event_types is not UNSET:
        params["eventTypes"] = event_types
    if poll is not UNSET:
        params["poll"] = poll

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[EventsPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = EventsPaginatedList.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json())

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[EventsPaginatedList, BadRequestError]]:
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
    created_atgte: Union[Unset, str] = UNSET,
    starting_after: Union[Unset, str] = UNSET,
    event_types: Union[Unset, str] = UNSET,
    poll: Union[Unset, bool] = UNSET,
) -> Response[Union[EventsPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        created_atgte=created_atgte,
        starting_after=starting_after,
        event_types=event_types,
        poll=poll,
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
    created_atgte: Union[Unset, str] = UNSET,
    starting_after: Union[Unset, str] = UNSET,
    event_types: Union[Unset, str] = UNSET,
    poll: Union[Unset, bool] = UNSET,
) -> Optional[Union[EventsPaginatedList, BadRequestError]]:
    """  """

    return sync_detailed(
        client=client,
        page_size=page_size,
        next_token=next_token,
        created_atgte=created_atgte,
        starting_after=starting_after,
        event_types=event_types,
        poll=poll,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    starting_after: Union[Unset, str] = UNSET,
    event_types: Union[Unset, str] = UNSET,
    poll: Union[Unset, bool] = UNSET,
) -> Response[Union[EventsPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        created_atgte=created_atgte,
        starting_after=starting_after,
        event_types=event_types,
        poll=poll,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    starting_after: Union[Unset, str] = UNSET,
    event_types: Union[Unset, str] = UNSET,
    poll: Union[Unset, bool] = UNSET,
) -> Optional[Union[EventsPaginatedList, BadRequestError]]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            page_size=page_size,
            next_token=next_token,
            created_atgte=created_atgte,
            starting_after=starting_after,
            event_types=event_types,
            poll=poll,
        )
    ).parsed
