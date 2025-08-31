from uuid_utils.compat import uuid4

from template.app.interactors.base import Command, Interactor
from template.app.interactors.transform import handler
from template.app.interfaces.repos.gateway import RepoGateway
from template.app.interfaces.repos.transaction_manager import TransactionManager
from template.app.interfaces.security.hasher import Hasher
from template.domain.entities.user import User
from template.presentation.http.common.dtos.user import PublicUser


class CreateUserCommand(Command):
    login: str
    password: str


@handler
class CreateUserInteractor(Interactor[CreateUserCommand, PublicUser]):
    repo_gateway: RepoGateway
    password_hasher: Hasher
    transaction_manager: TransactionManager

    async def _execute(self, cmd: CreateUserCommand) -> PublicUser:
        user = User(
            id=uuid4(),
            login=cmd.login,
            password_hash=self.password_hasher.hash(cmd.password),
        )
        user.validate_plain_password(cmd.password)
        async with self.transaction_manager:
            await self.repo_gateway.user().create(user)
        return PublicUser.from_(user)
