import pytest
from dishka import AsyncContainer
from uuid_utils.compat import uuid4

from template.app.errors import NotFoundError
from template.app.interactors.users.create import CreateUserForm, CreateUserInteractor
from template.app.interactors.users.get import GetUserForm, GetUserInteractor


async def test_get_user(container: AsyncContainer) -> None:
    async with container() as request_container:
        create = await request_container.get(CreateUserInteractor)
        created = await create(CreateUserForm(login="getuser", password="Password1!"))

        get = await request_container.get(GetUserInteractor)
        result = await get(GetUserForm(id=created.id))

        assert result.id == created.id
        assert result.login == "getuser"


async def test_get_user_not_found(container: AsyncContainer) -> None:
    async with container() as request_container:
        get = await request_container.get(GetUserInteractor)

        with pytest.raises(NotFoundError):
            await get(GetUserForm(id=uuid4()))
