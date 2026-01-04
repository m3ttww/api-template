import pytest
from dishka import AsyncContainer
from uuid_utils.compat import uuid4

from template.app.errors import NotFoundError
from template.app.interactors.users.create import CreateUserForm, CreateUserInteractor
from template.app.interactors.users.update import UpdateUserForm, UpdateUserInteractor


async def test_update_user_password(container: AsyncContainer) -> None:
    async with container() as request_container:
        create = await request_container.get(CreateUserInteractor)
        created = await create(
            CreateUserForm(login="updateuser", password="Password1!")
        )

        update = await request_container.get(UpdateUserInteractor)
        result = await update(UpdateUserForm(id=created.id, password="NewPassword1!"))

        assert result.id == created.id
        assert result.login == "updateuser"


async def test_update_user_not_found(container: AsyncContainer) -> None:
    async with container() as request_container:
        update = await request_container.get(UpdateUserInteractor)

        with pytest.raises(NotFoundError):
            await update(UpdateUserForm(id=uuid4(), password="Password1!"))
