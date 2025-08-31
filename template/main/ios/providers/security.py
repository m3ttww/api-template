from dishka import Provider, Scope, provide
from template.app.interfaces.security.hasher import Hasher

from template.infra.security.hasher import get_argon2_hasher


class SecurityProvider(Provider):
    scope = Scope.APP

    @provide
    def hasher(self) -> Hasher:
        return get_argon2_hasher()
