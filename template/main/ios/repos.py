from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from template.app.interfaces.repos.gateway import RepoGateway
from template.app.interfaces.repos.transaction_manager import TransactionManager
from template.infra.persistence import psql


class ReposProvider(Provider):
    scope = Scope.REQUEST

    @provide()
    async def transaction_manager(
        self, session: AsyncSession
    ) -> AsyncIterable[TransactionManager]:
        yield psql.TransactionManagerImpl(session)

    @provide()
    async def repo_gateway(self, session: AsyncSession) -> AsyncIterable[RepoGateway]:
        yield psql.RepoGatewayImpl(session)
