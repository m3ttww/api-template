from src.presentation.http.v1.common.dtos.base import DTO


class PublicUser(DTO):
    id: str
    login: str
