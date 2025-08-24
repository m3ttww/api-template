from template.domain.entities.base import Entity, IDType



class WithOwner(Entity):
    owner_id: IDType
