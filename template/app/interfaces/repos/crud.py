from typing import Any, Mapping, Protocol, runtime_checkable

from template.app.interfaces.option import Option
from template.domain.entities.base import Entity, IDType


@runtime_checkable
class CRUDRepo[E: Entity](Protocol):
    async def create(self, entity: E) -> None: ...

    async def get_by_id(self, id_: IDType) -> Option[E]: ...

    async def update(self, id_: IDType, data: Mapping[str, Any]) -> Option[E]: ...

    async def delete(self, id_: IDType) -> None: ...

    async def get_all(self, data: Mapping[str, Any]) -> list[E]: ...
