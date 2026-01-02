from abc import abstractmethod

from template.app.interfaces.option import Option
from template.app.interfaces.repos.crud import CRUDRepo
from template.domain.entities.user import User


class UserRepo(CRUDRepo[User]):
    @abstractmethod
    async def get_by_login(self, login: str) -> Option[User]: ...
