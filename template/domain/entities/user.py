from template.domain.entities.base import Entity
from template.domain.entities.mixins.with_id import WithId


class User(WithId, Entity):
    login: str
    password_hash: str
