from template.app.dtos.user import PublicUser
from template.app.errors import NotFoundError
from template.app.interactors.base import Form, Interactor
from template.app.interactors.transform import interactor
from template.app.interfaces.repos.gateway import RepoGateway
from template.domain.entities.base import IDType


class GetUserForm(Form):
    id: IDType


@interactor
class GetUserInteractor(Interactor[GetUserForm, PublicUser]):
    repo_gateway: RepoGateway

    async def _execute(self, form: GetUserForm) -> PublicUser:
        user = await self.repo_gateway.user().get_by_id(form.id)
        return PublicUser.from_(
            user.some(NotFoundError(message="User not found", status_code=404))
        )
