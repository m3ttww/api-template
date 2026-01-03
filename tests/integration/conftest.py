from collections.abc import Iterator
from urllib.parse import urlparse

import pytest
from alembic import command
from alembic.config import Config as AlembicConfig
from dishka import AsyncContainer
from testcontainers.postgres import PostgresContainer  # type: ignore[import-untyped]

from template.internal.root import get_root_path
from template.main.ioс.container import create_container
from template.main.settings import Settings


@pytest.fixture(scope="session")
def postgres() -> Iterator[PostgresContainer]:
    with PostgresContainer(
        image="postgres:16",
        username="postgres",
        password="postgres",
        dbname="template",
    ) as pg:
        yield pg


@pytest.fixture(scope="session")
def settings(postgres: PostgresContainer) -> Settings:
    url = urlparse(postgres.get_connection_url())
    return Settings(
        POSTGRES_DRIVER="asyncpg",
        POSTGRES_USER="postgres",
        POSTGRES_PASS="postgres",
        POSTGRES_HOST=url.hostname or "localhost",
        POSTGRES_PORT=str(url.port or 5432),
        POSTGRES_DB="template",
        POSTGRES_POOL_SIZE=10,
        POSTGRES_MAX_OVERFLOW=2,
        LOG_LEVEL="INFO",
    )


@pytest.fixture(scope="session")
def _migrations(settings: Settings) -> None:
    persistence_path = get_root_path() / "template" / "infra" / "persistence"
    alembic_config = AlembicConfig(persistence_path / "alembic.ini")
    alembic_config.set_main_option(
        "script_location", str(persistence_path / "migrations")
    )
    alembic_config.set_main_option("sqlalchemy.url", settings.get_postgres_url())
    command.upgrade(alembic_config, "head")


@pytest.fixture
def container(settings: Settings, _migrations: None) -> AsyncContainer:
    return create_container(settings)
