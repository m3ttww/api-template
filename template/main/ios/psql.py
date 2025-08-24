from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from template.main.settings import Settings

class PostgresProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    def async_engine(self, config: Settings) -> AsyncEngine:
        return create_async_engine(
            config.get_postgres_url(),
            pool_size=config.POSTGRES_POOL_SIZE,
            max_overflow=config.POSTGRES_MAX_OVERFLOW,
        )

    @provide(scope=Scope.APP)
    def async_session_maker(
        self, async_engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(async_engine, expire_on_commit=False, autoflush=False)

    @provide()
    async def async_session(
        self, async_session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with async_session_maker() as session:
            yield session
