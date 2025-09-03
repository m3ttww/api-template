from litestar import Controller, post, Request
from litestar.status_codes import HTTP_201_CREATED
from dishka import FromDishka
from template.app.interactors.users.create import (
    CreateUserCommand,
    CreateUserInteractor,
)
from template.app import dtos

class UserController(Controller):
    path = "/users"
    tags = ["User"]

    @post(summary="Create a new user", status_code=HTTP_201_CREATED)
    async def create_user_endpoint(
        self,
        data: CreateUserCommand,
        request: Request,
        interactor: FromDishka[CreateUserInteractor],
    ) -> dtos.PublicUser:
        request.state
        return await interactor(data)
