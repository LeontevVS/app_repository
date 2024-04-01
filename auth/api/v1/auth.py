from fastapi import APIRouter, Response, Request

from services.auth import DEFAULT_EXP_REFRESH_SECONDS
from depends.auth import auth_service


router = APIRouter(tags=['auth'], prefix='/auth')


@router.post('/refresh/')
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


@router.post('/')
async def get_access_token(request: Request):
    refresh_token = request.cookies.get('refresh_token', '')
    access_token = await auth_service.get_access_token(refresh_token)
    return {
        'access_token': access_token,
        'type': 'Bearer',
    }
