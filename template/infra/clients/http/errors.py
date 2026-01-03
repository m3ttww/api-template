from collections.abc import Sequence
from typing import Any


class NetworkError(Exception):
    __slots__ = ()

    def __init__(
        self, message: str = "Request timed out", errors: Sequence[Any] | None = None
    ) -> None:
        super().__init__(message, errors)
