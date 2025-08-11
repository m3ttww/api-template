from uuid import UUID

from src.domain.entities.base import Entity

type IDType = UUID


class WithId(Entity):
    id: IDType
