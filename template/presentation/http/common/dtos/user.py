from template.presentation.http.common.dtos.base import DTO


class PublicUser(DTO):
    id: str
    login: str
