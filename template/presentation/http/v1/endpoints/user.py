from typing import Annotated

from fastapi import APIRouter, Depends, status
from template.presentation.http.v1.common import dtos

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.post(
    "",
    status_code=status.HTTP_200_OK,
)
async def create_user_endpoint(
    body: dtos.CreateUser,
    interactor: Annotated[InteractorProtocol, Depends()],
) -> dtos.PublicUser:
    return await interactor(body)
