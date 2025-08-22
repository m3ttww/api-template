from uuid import UUID

from template.domain.entities.base import Entity

type IDType = UUID


class WithId(Entity):
    id: IDType
