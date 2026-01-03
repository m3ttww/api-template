from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any, Protocol, Self

if TYPE_CHECKING:
    from collections.abc import Mapping
    from types import TracebackType

    from aiohttp import StreamReader

    from template.infra.clients.http.types import RequestMethodType


class JsonResponse(Protocol):
    async def json(self, **kwargs: Any) -> Any: ...


class TextResponse(Protocol):
    async def text(self, **kwargs: Any) -> str: ...


class BytesResponse(Protocol):
    async def read(self) -> bytes: ...


class UrlResponse(Protocol):
    @property
    def url(self) -> str: ...


class StatusResponse(Protocol):
    @property
    def status(self) -> int: ...

    @property
    def ok(self) -> bool: ...


class HeadersResponse(Protocol):
    @property
    def headers(self) -> Mapping[str, object]: ...


class CookiesResponse(Protocol):
    @property
    def cookies(self) -> Mapping[str, object]: ...


class ContentResponse(Protocol):
    @property
    def content(self) -> StreamReader: ...


class CloseableResponse(Protocol):
    def close(self) -> None: ...


class Response(
    JsonResponse,
    TextResponse,
    BytesResponse,
    HeadersResponse,
    CookiesResponse,
    UrlResponse,
    StatusResponse,
    ContentResponse,
    CloseableResponse,
):
    pass


class AsyncHTTPClient(abc.ABC):
    __slots__ = (
        "manager",
        "url",
    )

    def __init__(
        self,
        url: str | None = None,
    ) -> None:
        self.url = url

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.close_session()

    async def __call__(
        self,
        method: RequestMethodType,
        url_or_endpoint: str,
        data: object | None = None,
        json: Mapping[str | int, object] | None = None,
        headers: Mapping[str, object] | None = None,
        params: Mapping[str, object] | None = None,
        request_timeout: int | None = 10,
        stream: bool = False,  # noqa: FBT001, FBT002
    ) -> Response:
        return await self.make_request(
            method=method,
            url_or_endpoint=url_or_endpoint,
            data=data,
            json=json,
            headers=headers,
            params=params,
            request_timeout=request_timeout,
            stream=stream,
        )

    @abc.abstractmethod
    async def make_request(
        self,
        method: RequestMethodType,
        url_or_endpoint: str,
        data: object | None = None,
        json: Mapping[str | int, object] | None = None,
        headers: Mapping[str, object] | None = None,
        params: Mapping[str, object] | None = None,
        request_timeout: int | None = 10,
        stream: bool = False,  # noqa: FBT001, FBT002
    ) -> Response:
        raise NotImplementedError

    @abc.abstractmethod
    async def close_session(self) -> None:
        raise NotImplementedError
