from template.domain.entities.base import IDType
from template.internal.tools.dto import DTO


class PublicUser(DTO):
    id: IDType
    login: str
