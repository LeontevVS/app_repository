from typing import Annotated

from fastapi import APIRouter, Response, Request, Header

from services.auth import DEFAULT_EXP_REFRESH_SECONDS
from depends.auth import auth_service


private_router = APIRouter(tags=['auth'])
public_router = APIRouter(tags=['auth'], prefix='/public')


@public_router.post('/refresh/')
async def get_token_couple(response: Response, request: Request):
    # TODO: add removing refresh tokens if token was deactivated
    refresh_token = request.cookies.get('refresh_token', '')
    tokens = await auth_service.reissue_tokens(refresh_token)
    response.set_cookie(
        key='refresh_token',
        value=tokens.refresh_token,
        max_age=DEFAULT_EXP_REFRESH_SECONDS,
    )
    return {
        'access_token': tokens.access_token,
        'type': 'Bearer',
    }


@public_router.post('/access/')
async def get_access_token(request: Request):
    refresh_token = request.cookies.get('refresh_token', '')
    access_token = await auth_service.get_access_token(refresh_token)
    return {
        'access_token': access_token,
        'type': 'Bearer',
    }


@public_router.post('/')
async def authenticate(access_token: Annotated[str | None, Header()]):
    return await auth_service.get_token_info(access_token)


@public_router.post('/logout/')
async def logout_user(request: Request):
    refresh_token = request.cookies.get('refresh_token', '')
    await auth_service.remove_refresh_token(refresh_token)
    return {'status': 'ok'}
