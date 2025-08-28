from dishka import FromDishka 
from fastapi import APIRouter, status

from template.app.interactors.users.create import CreateUserCommand, CreateUserInteractor
from template.presentation.http.common import dtos

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.post(
    "",
    description="Create a new user",
    status_code=status.HTTP_201_CREATED,
)
async def create_user_endpoint(
    body: CreateUserCommand,
    interactor: FromDishka[CreateUserInteractor],
) -> dtos.PublicUser:
    return await interactor(body)
