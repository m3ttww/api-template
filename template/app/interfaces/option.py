from abc import abstractmethod
from typing import Protocol


class Option[T](Protocol):
    value: T | None

    @abstractmethod
    def some(self, exc: Exception) -> T: ...

    @abstractmethod
    def none(self, exc: Exception) -> None: ...

    @abstractmethod
    def some_or[R](self, default: R) -> T | R: ...
