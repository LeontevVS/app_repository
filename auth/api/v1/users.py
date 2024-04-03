from fastapi import APIRouter, Response, Request

from depends.auth_users import auth_user_service
from schemas.users import UserLogInDTO, UserSignInDTO
from services.auth.consts import DEFAULT_EXP_REFRESH_SECONDS

private_router = APIRouter(tags=['users'], prefix='/users')
public_router = APIRouter(tags=['auth'], prefix='/users/public')


@public_router.post('/login/')
async def login_user(response: Response, user: UserLogInDTO):
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


@public_router.post('/signin/')
async def register_user(response: Response, user: UserSignInDTO):
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
