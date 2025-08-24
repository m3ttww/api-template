from abc import abstractmethod
from typing import Protocol


class Hasher(Protocol):
    __slots__ = ()

    @abstractmethod
    def hash(self, data: str) -> str: ...

    @abstractmethod
    def verify(self, data: str, hash_: str) -> bool: ...
