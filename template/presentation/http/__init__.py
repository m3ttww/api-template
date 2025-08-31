__all__ = ("create_router",)

from litestar import Router

from .v1 import create_v1_router


def create_router() -> Router:
    return Router(
        path="/api",
        route_handlers=[create_v1_router()],
    )
