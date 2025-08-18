from abc import abstractmethod
from typing import Protocol

from src.domain.entities.base import Entity
from src.presentation.http.v1.common.dtos import DTO


class Command(DTO): ...


class Interactor[C: Command, R: DTO | Entity | None](Protocol):
    async def __call__(self, cmd: C) -> R:
        return await self._handle(cmd)

    @abstractmethod
    async def _handle(self, cmd: C, /) -> R:
        raise NotImplementedError
