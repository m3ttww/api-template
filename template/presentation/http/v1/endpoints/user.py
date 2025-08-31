from litestar import Controller, post
from litestar.status_codes import HTTP_201_CREATED
from dishka import FromDishka
from template.app.interactors.users.create import (
    CreateUserCommand,
    CreateUserInteractor,
)
from template.presentation.http.common import dtos


class UserController(Controller):
    path = "/users"
    tags = ["User"]

    @post(summary="Create a new user", status_code=HTTP_201_CREATED)
    async def create_user_endpoint(
        self,
        data: CreateUserCommand,
        interactor: FromDishka[CreateUserInteractor],
    ) -> dtos.PublicUser:
        return await interactor(data)
