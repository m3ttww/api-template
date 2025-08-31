from abc import abstractmethod
from typing import Protocol

from template.domain.entities.base import Entity
from template.internal.tools.dto import DTO


class Command(DTO): ...


class Interactor[C: Command, R: DTO | Entity | None](Protocol):
    async def __call__(self, cmd: C) -> R:
        return await self._execute(cmd)

    @abstractmethod
    async def _execute(self, cmd: C, /) -> R:
        raise NotImplementedError
