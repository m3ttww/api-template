from dishka import Provider

from .interactors import create_interactors_provider
from .psql import PostgresProvider
from .repos import ReposProvider
from .security import SecurityProvider


def get_providers() -> list[Provider]:
    return [
        SecurityProvider(),
        PostgresProvider(),
        ReposProvider(),
        create_interactors_provider(),
    ]


__all__ = ("get_providers",)
