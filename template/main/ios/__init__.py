from dishka import Provider

from template.main.ios.providers.handlers import HandlersProvider
from template.main.ios.providers.psql import PostgresProvider
from template.main.ios.providers.repos import ReposProvider


def get_providers() -> list[Provider]:
    return [
        PostgresProvider(),
        ReposProvider(),
        HandlersProvider(),
    ]


__all__ = ("get_providers",)
