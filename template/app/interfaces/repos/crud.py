from abc import abstractmethod
from typing import Protocol, runtime_checkable

from template.app.interfaces.option import Option
from template.domain.entities.base import Entity, IDType


@runtime_checkable
class CRUDRepo[E: Entity](Protocol):
    @abstractmethod
    async def create(self, entity: E) -> None: ...

    @abstractmethod
    async def get_by_id(self, id_: IDType) -> Option[E]: ...

    @abstractmethod
    async def update(self, entity: E, /) -> None: ...

    @abstractmethod
    async def delete(self, entity: E, /) -> None: ...
