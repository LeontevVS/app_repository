from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from utils_backend.auth.authorize import authorize, PrivateUserRoles
from .models import UserOutViewModel
from modules.users.user.services.user_service import get_user_service, UserServiceP

user_router = APIRouter(prefix="/user")


@user_router.get(
    path="/list",
    dependencies=[
        Depends(
            authorize(roles=[PrivateUserRoles.ADMIN])
        ),
    ]
)
async def get_users_list(
    user_service: Annotated[UserServiceP, Depends(get_user_service)],
    limit: int,
    offset: int,
) -> list[UserOutViewModel]:
    users = await user_service.get_users(
        limit=limit,
        offset=offset,
    )
    return [UserOutViewModel(**user.model_dump()) for user in users]


@user_router.get(
    path="/{user_id}",
    dependencies=[
        Depends(
            authorize(roles=[PrivateUserRoles.ADMIN])
        ),
    ]
)
async def get_user(
    user_service: Annotated[UserServiceP, Depends(get_user_service)],
    user_id: UUID,
) -> UserOutViewModel:
    user = await user_service.get_user(user_id=user_id)
    return UserOutViewModel(**user.model_dump())
