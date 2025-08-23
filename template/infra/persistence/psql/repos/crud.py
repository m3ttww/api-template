from typing import Any, Mapping, cast, get_args, get_origin

from sqlalchemy.ext.asyncio import AsyncSession

from template.app.interfaces.repos.crud import CRUDRepo
from template.domain.entities.base import Entity, IDType
from template.infra.option import Option


class CRUDRepoImpl[E: Entity](CRUDRepo[E]):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, entity: E, /) -> None:
        self._session.add(entity)

    async def update(self, id_: IDType, data: Mapping[str, Any], /) -> Option[E]:
        entity = await self._session.get(self.entity, id_)
        if entity:
            for key, value in data.items():
                field = getattr(entity, key)
                if not field:
                    raise ValueError(f"Field {key} not found in entity {entity}")
                setattr(entity, key, value)
            await self._session.merge(entity)
        return Option(entity)

    async def get_by_id(self, id_: IDType, /) -> Option[E]:
        return Option(await self._session.get(self.entity, id_))

    async def delete(self, id_: IDType, /) -> None:
        entity = await self._session.get(self.entity, id_)
        if entity:
            await self._session.delete(entity)

    @property
    def entity(self) -> type[E]:
        for base in self.__orig_bases__:  # type: ignore[attr-defined]
            cls = get_origin(base)
            if issubclass(cls, CRUDRepo):
                break
        else:
            msg = "CRUDRepo not found"
            raise ValueError(msg)

        bound_entity, *_nothing = get_args(base)
        return cast("type[E]", bound_entity)
