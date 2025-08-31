__all__ = ("create_v1_router",)

from dishka.integrations.litestar import DishkaRouter

from .user import UserController


def create_v1_router() -> DishkaRouter:
    return DishkaRouter(
        path="/v1",
        route_handlers=[
            UserController,
        ],
    )
