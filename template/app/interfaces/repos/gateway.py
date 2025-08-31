from abc import abstractmethod
from typing import Protocol

from template.app.interfaces.repos.user import UserRepo


class RepoGateway(Protocol):
    @abstractmethod
    def user(self) -> UserRepo: ...
