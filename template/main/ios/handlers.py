from typing import AsyncIterable
from dishka import Provider, Scope, provide

from template.app.interactors.users.create import CreateUserInteractor
from template.app.interfaces.repos.gateway import RepoGateway
from template.app.interfaces.repos.transaction_manager import TransactionManager
from template.app.interfaces.security.hasher import Hasher


class HandlersProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def create_user_handler(
        self,
        repo_gateway: RepoGateway,
        password_hasher: Hasher,
        transaction_manager: TransactionManager,
    ) -> AsyncIterable[CreateUserInteractor]:
        yield CreateUserInteractor(repo_gateway, password_hasher, transaction_manager)
