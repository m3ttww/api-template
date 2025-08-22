from template.domain.entities.base import Entity

from .with_id import IDType


class WithOwner(Entity):
    owner_id: IDType
