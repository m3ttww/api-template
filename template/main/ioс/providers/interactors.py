from dishka import Provider, Scope

from template.app.interactors import get_defined_interactors


def create_interactors_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    for interactor in get_defined_interactors().values():
        provider.provide(interactor, provides=interactor)
    return provider
