from template.app.dtos.user import PublicUser
from template.app.errors import NotFoundError
from template.app.interactors.base import Form, Interactor
from template.app.interactors.transform import interactor
from template.app.interfaces.repos.gateway import RepoGateway
from template.app.interfaces.repos.transaction_manager import TransactionManager
from template.app.interfaces.security.hasher import Hasher
from template.domain.entities.base import IDType


class UpdateUserForm(Form):
    id: IDType
    password: str


@interactor
class UpdateUserInteractor(Interactor[UpdateUserForm, PublicUser]):
    repo_gateway: RepoGateway
    transaction_manager: TransactionManager
    password_hasher: Hasher

    async def _execute(self, form: UpdateUserForm) -> PublicUser:
        user_repo = self.repo_gateway.user()

        user_option = await user_repo.get_by_id(form.id)
        user = user_option.some(
            NotFoundError(message="User not found", status_code=404)
        )

        user.validate_plain_password(form.password)
        user.password_hash = self.password_hasher.hash(form.password)

        async with self.transaction_manager:
            await user_repo.update(user)

        return PublicUser.from_(user)
