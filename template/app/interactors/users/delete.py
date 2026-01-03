from template.app.errors import NotFoundError
from template.app.interactors.base import Form, Interactor
from template.app.interactors.transform import interactor
from template.app.interfaces.repos.gateway import RepoGateway
from template.app.interfaces.repos.transaction_manager import TransactionManager
from template.domain.entities.base import IDType


class DeleteUserForm(Form):
    id: IDType


@interactor
class DeleteUserInteractor(Interactor[DeleteUserForm, None]):
    repo_gateway: RepoGateway
    transaction_manager: TransactionManager

    async def _execute(self, form: DeleteUserForm) -> None:
        user_repo = self.repo_gateway.user()

        user = (await user_repo.get_by_id(form.id)).some(
            NotFoundError(message="User not found", status_code=404)
        )

        async with self.transaction_manager:
            await user_repo.delete(user)
