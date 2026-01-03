from uuid_utils.compat import uuid4

from template.app.dtos.user import PublicUser
from template.app.errors import ConflictError
from template.app.interactors.base import Form, Interactor
from template.app.interactors.transform import interactor
from template.app.interfaces.repos.gateway import RepoGateway
from template.app.interfaces.repos.transaction_manager import TransactionManager
from template.app.interfaces.security.hasher import Hasher
from template.domain.entities.user import User


class CreateUserForm(Form):
    login: str
    password: str


@interactor
class CreateUserInteractor(Interactor[CreateUserForm, PublicUser]):
    repo_gateway: RepoGateway
    password_hasher: Hasher
    transaction_manager: TransactionManager

    async def _execute(self, form: CreateUserForm) -> PublicUser:
        existing_user = await self.repo_gateway.user().get_by_login(form.login)
        existing_user.none(
            ConflictError(
                message="User with this login already exists",
                status_code=409,
            )
        )

        user = User(
            id=uuid4(),
            login=form.login,
            password_hash=self.password_hasher.hash(form.password),
        )
        user.validate()
        user.validate_plain_password(form.password)
        async with self.transaction_manager:
            await self.repo_gateway.user().create(user)
        return PublicUser.from_(user)
