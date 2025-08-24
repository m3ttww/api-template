from template.app.interfaces.repos.gateway import RepoGateway
from template.app.interfaces.repos.user import UserRepo
from template.infra.persistence.psql.repos.user import UserRepoImpl
from sqlalchemy.ext.asyncio import AsyncSession

class RepoGatewayImpl(RepoGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def user(self) -> UserRepo:
        return UserRepoImpl(self._session)