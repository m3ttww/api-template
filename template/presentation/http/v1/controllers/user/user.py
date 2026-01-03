from litestar import Controller, delete, get, patch, post
from litestar.status_codes import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from template.app import dtos
from template.app.interactors.users.create import CreateUserForm, CreateUserInteractor
from template.app.interactors.users.delete import DeleteUserForm, DeleteUserInteractor
from template.app.interactors.users.get import GetUserForm, GetUserInteractor
from template.app.interactors.users.update import UpdateUserForm, UpdateUserInteractor
from template.domain.entities.base import IDType
from template.internal.di import Depends
from template.presentation.http.v1.controllers.user.dto import UpdatePassword


class UserController(Controller):
    path = "/users"
    tags = ["User"]

    @post(summary="Create a new user", status_code=HTTP_201_CREATED)
    async def create_user(
        self,
        data: CreateUserForm,
        interactor: Depends[CreateUserInteractor],
    ) -> dtos.PublicUser:
        return await interactor(data)

    @get("/{user_id:uuid}", summary="Get user by ID")
    async def get_user(
        self,
        user_id: IDType,
        interactor: Depends[GetUserInteractor],
    ) -> dtos.PublicUser:
        return await interactor(GetUserForm(id=user_id))

    @patch("/{user_id:uuid}", summary="Update user password")
    async def update_user(
        self,
        user_id: IDType,
        data: UpdatePassword,
        interactor: Depends[UpdateUserInteractor],
    ) -> dtos.PublicUser:
        return await interactor(UpdateUserForm(id=user_id, password=data.password))

    @delete("/{user_id:uuid}", summary="Delete user", status_code=HTTP_204_NO_CONTENT)
    async def delete_user(
        self,
        user_id: IDType,
        interactor: Depends[DeleteUserInteractor],
    ) -> None:
        await interactor(DeleteUserForm(id=user_id))
