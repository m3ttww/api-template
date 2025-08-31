from dishka import Provider

from .handlers import HandlersProvider
from .psql import PostgresProvider
from .repos import ReposProvider
from .security import SecurityProvider


def get_providers() -> list[Provider]:
    return [
        SecurityProvider(),
        PostgresProvider(),
        ReposProvider(),
        HandlersProvider(),
    ]


__all__ = ("get_providers",)
