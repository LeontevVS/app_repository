from fastapi import (
    APIRouter,
    Depends,
    Response,
    Cookie,
)

from schemas.auth import AuthDTO
from services.auth.consts import DEFAULT_EXP_REFRESH_SECONDS
from depends.auth import auth_service

router = APIRouter(tags=['auth'], prefix='/auth')


@router.post('/refresh/')
async def get_token_couple(
    response: Response,
    refresh_token=Cookie(),
):
    access_token = await auth_service.get_access_token(refresh_token)
    response.set_cookie(
        key='refresh_token',
        value=...,
        max_age=DEFAULT_EXP_REFRESH_SECONDS,
    )
    return {
        'access_token': access_token,
        'type': 'Bearer',
    }


@router.post('/auth/')
async def get_access_token(refresh_token=Cookie()):
    access_token = await auth_service.get_access_token(refresh_token)
    return {
        'access_token': access_token,
        'type': 'Bearer',
    }
