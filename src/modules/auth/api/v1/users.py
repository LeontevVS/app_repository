from fastapi import APIRouter, Depends, Response

from src.modules.auth.depends.auth_users import get_auth_user_service
from src.modules.auth.schemas.users import UserLogInDTO, UserSignInDTO
from src.modules.auth.services.auth.consts import DEFAULT_EXP_REFRESH_SECONDS
from src.modules.auth.services.auth_users import AuthUserService

router = APIRouter(tags=['users'], prefix='/users')


@router.post('/login/')
async def auth_user(
    response: Response,
    user: UserLogInDTO,
    auth_user_service: AuthUserService = Depends(get_auth_user_service),
):
    tokens = await auth_user_service.login_user(user)
    response.set_cookie(
        key='refresh_token',
        value=tokens.refresh_token,
        max_age=DEFAULT_EXP_REFRESH_SECONDS,
    )
    return {
        'access_token': tokens.access_token,
        'type': 'Bearer',
    }


@router.post('/signin/')
async def register_user(
    response: Response,
    user: UserSignInDTO,
    auth_user_service: AuthUserService = Depends(get_auth_user_service),
):
    tokens = await auth_user_service.signin_user(user)
    response.set_cookie(
        key='refresh_token',
        value=tokens.refresh_token,
        max_age=DEFAULT_EXP_REFRESH_SECONDS,
    )
    return {
        'access_token': tokens.access_token,
        'type': 'Bearer',
    }
