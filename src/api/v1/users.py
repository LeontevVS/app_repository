from fastapi import APIRouter, Depends, Response

from depends.auth_users import auth_user_service
from schemas.users import UserLogInDTO, UserSignInDTO
from services.auth.consts import DEFAULT_EXP_REFRESH_SECONDS


router = APIRouter(tags=['users'], prefix='/users')


@router.post('/login/')
async def auth_user(
    response: Response,
    user: UserLogInDTO = Depends(),
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
    user: UserSignInDTO = Depends(),
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
