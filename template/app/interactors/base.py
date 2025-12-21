from abc import abstractmethod
from typing import ClassVar, Protocol, get_args

from template.domain.entities.base import Entity
from template.internal.tools.dto import DTO


class Command(DTO): ...


class Interactor[C: Command, R: DTO | Entity | None](Protocol):
    command_cls: ClassVar[type[Command]]

    def __init_subclass__(cls, /) -> None:
        cls.command_cls = get_args(cls.__orig_bases__[-1])[0]  # type: ignore[attr-defined]

    async def __call__(self, cmd: C) -> R:
        return await self._execute(cmd)

    @abstractmethod
    async def _execute(self, cmd: C, /) -> R:
        raise NotImplementedError
