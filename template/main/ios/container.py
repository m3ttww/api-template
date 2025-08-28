from dishka import AsyncContainer, Provider, make_async_container

from template.main.ios import get_providers
from template.main.settings import Settings


def create_container(
    config: Settings, providers: list[Provider] | None = None
) -> AsyncContainer:
    if providers is None:
        providers = get_providers()
    return make_async_container(*providers, context={Settings: config})
