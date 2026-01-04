import pytest
from dishka import AsyncContainer

from template.app.errors import ConflictError
from template.app.interactors.users.create import CreateUserForm, CreateUserInteractor


async def test_create_user(container: AsyncContainer) -> None:
    async with container() as request_container:
        interactor = await request_container.get(CreateUserInteractor)
        result = await interactor(
            CreateUserForm(login="testuser", password="Password1!")
        )

        assert result.login == "testuser"
        assert result.id is not None


async def test_create_user_duplicate_login(container: AsyncContainer) -> None:
    async with container() as request_container:
        interactor = await request_container.get(CreateUserInteractor)
        await interactor(CreateUserForm(login="duplicate", password="Password1!"))

        with pytest.raises(ConflictError):
            await interactor(CreateUserForm(login="duplicate", password="Password1!"))
