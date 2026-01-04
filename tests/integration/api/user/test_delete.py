import pytest
from dishka import AsyncContainer
from uuid_utils.compat import uuid4

from template.app.errors import NotFoundError
from template.app.interactors.users.create import CreateUserForm, CreateUserInteractor
from template.app.interactors.users.delete import DeleteUserForm, DeleteUserInteractor
from template.app.interactors.users.get import GetUserForm, GetUserInteractor


async def test_delete_user(container: AsyncContainer) -> None:
    async with container() as request_container:
        create = await request_container.get(CreateUserInteractor)
        created = await create(
            CreateUserForm(login="deleteuser", password="Password1!")
        )

        delete = await request_container.get(DeleteUserInteractor)
        await delete(DeleteUserForm(id=created.id))

        get = await request_container.get(GetUserInteractor)
        with pytest.raises(NotFoundError):
            await get(GetUserForm(id=created.id))


async def test_delete_user_not_found(container: AsyncContainer) -> None:
    async with container() as request_container:
        delete = await request_container.get(DeleteUserInteractor)

        with pytest.raises(NotFoundError):
            await delete(DeleteUserForm(id=uuid4()))
