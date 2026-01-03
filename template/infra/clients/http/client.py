from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from logging import getLogger
from typing import (
    TYPE_CHECKING,
    Any,
    ParamSpec,
)

import orjson
from aiohttp import (
    BaseConnector,
    ClientConnectionResetError,
    ClientError,
    ClientResponse,
    ClientSession,
    ClientTimeout,
    StreamReader,
    TCPConnector,
)

from template.infra.clients.http.base import AsyncHTTPClient, Response
from template.infra.clients.http.errors import NetworkError
from template.infra.clients.http.types import (
    RequestMethodType,
)

logger = getLogger(__name__)

if TYPE_CHECKING:
    from collections.abc import Mapping

P = ParamSpec("P")


class ClientResponseAdapter(Response):
    __slots__ = (
        "_origin_response",
        "_raw_content",
    )

    def __init__(
        self,
        origin_response: ClientResponse,
        raw_content: bytes = b"",
    ) -> None:
        self._origin_response = origin_response
        self._raw_content = raw_content

    def __repr__(self) -> str:
        return f"{type(self).__name__}(url={self.url!r}, status={self.status!r})"

    async def __aenter__(self) -> "ClientResponseAdapter":
        return self

    async def __aexit__(self, *args: object) -> None:
        self.close()

    def __aiter__(self) -> "ClientResponseAdapter":
        return self

    async def __anext__(self) -> bytes:
        chunk = await self._origin_response.content.read(8192)
        if not chunk:
            raise StopAsyncIteration
        return chunk

    async def iter_chunks(self, chunk_size: int = 8192) -> AsyncIterator[bytes]:
        async for chunk in self._origin_response.content.iter_chunked(chunk_size):
            yield chunk

    async def iter_lines(self) -> AsyncIterator[bytes]:
        async for line in self._origin_response.content:
            yield line

    async def json(self, **kwargs: Any) -> Any:
        encoding = kwargs.pop("encoding", "utf-8")
        if not self._raw_content:
            self._raw_content = await self._origin_response.read()
        stripped = self._raw_content.strip()
        return orjson.loads(stripped.decode(encoding), **kwargs)

    async def read(self) -> bytes:
        if not self._raw_content:
            self._raw_content = await self._origin_response.read()
        return self._raw_content

    async def text(self, **kwargs: Any) -> str:
        encoding, errors = (
            kwargs.get("encoding", "utf-8"),
            kwargs.get("errors", "strict"),
        )
        if not self._raw_content:
            self._raw_content = await self._origin_response.read()
        return self._raw_content.decode(encoding=encoding, errors=errors)

    @property
    def status(self) -> int:
        return self._origin_response.status

    @property
    def ok(self) -> bool:
        return self._origin_response.ok

    @property
    def content(self) -> StreamReader:
        return self._origin_response.content

    @property
    def url(self) -> str:
        return str(self._origin_response.url)

    @property
    def headers(self) -> Mapping[str, object]:
        return self._origin_response.headers

    @property
    def cookies(self) -> Mapping[str, object]:
        return self._origin_response.cookies

    def close(self) -> None:
        if not self._origin_response.closed:
            self._origin_response.close()


class AiohttpClient(AsyncHTTPClient):
    __slots__ = (
        "_session",
        "_connector",
        "url",
    )

    def __init__(
        self,
        url: str | None = None,
        connector: BaseConnector | None = None,
    ) -> None:
        self.url = url
        self._session: ClientSession | None = None
        self._connector = connector

    async def create_session(self) -> ClientSession:
        if self._session is None or self._session.closed:
            connector = self._connector or TCPConnector(
                limit=500,
                limit_per_host=80,
                force_close=False,
                enable_cleanup_closed=True,
                keepalive_timeout=120,
                ttl_dns_cache=300,
                use_dns_cache=True,
            )
            self._session = ClientSession(
                connector=connector, timeout=ClientTimeout(total=120, connect=15)
            )

        return self._session

    async def close_session(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()
            await asyncio.sleep(0.25)

    async def make_request(
        self,
        method: RequestMethodType,
        url_or_endpoint: str,
        data: Any | None = None,
        json: Mapping[str | int, object] | None = None,
        headers: Mapping[str, Any] | None = None,
        params: Mapping[str, Any] | None = None,
        request_timeout: int | None = 10,
        stream: bool = False,  # noqa: FBT001, FBT002
    ) -> Response:
        session = await self.create_session()
        try:
            response = await session.request(
                method=method,
                url=url_or_endpoint,
                data=data,
                json=json,
                headers=headers,
                params=params,
                timeout=ClientTimeout(total=request_timeout),
            )
            if stream:
                return ClientResponseAdapter(response)
            content = await response.read()
            return ClientResponseAdapter(response, content)
        except TimeoutError as e:
            logger.exception(
                "Timeout while making request to %s with timeout %s",
                url_or_endpoint,
                request_timeout,
            )
            raise NetworkError from e
        except ClientConnectionResetError as e:
            logger.exception(
                "Connection reset while making request to %s with timeout %s",
                url_or_endpoint,
                request_timeout,
            )
            message_error = "Connection was reset"
            raise NetworkError(message_error) from e
        except ClientError as e:
            message_error = f"{type(e).__name__} occurred"
            logger.exception(
                "ClientError while making request to %s with timeout %s and error %s",
                url_or_endpoint,
                request_timeout,
                type(e).__name__,
            )
            raise NetworkError(message_error) from e
