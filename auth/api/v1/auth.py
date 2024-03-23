from fastapi import (
    APIRouter,
    Depends,
    Response,
    Request,
)

from depends.auth_users import user_permission
from services.auth import AuthService
from services.auth import DEFAULT_EXP_REFRESH_SECONDS
from depends.auth import get_auth_service


router = APIRouter(tags=['auth'], prefix='/auth')


@router.post('/refresh/')
async def get_token_couple(
    response: Response,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
):
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
async def get_access_token(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
):
    refresh_token = request.cookies.get('refresh_token', '')
    access_token = await auth_service.get_access_token(refresh_token)
    return {
        'access_token': access_token,
        'type': 'Bearer',
    }


@router.post('/admin')
async def get_access_token(
    user_info=Depends(user_permission.auth_admin_permissions)
):
    return user_info


@router.post('/seller')
async def get_access_token(
    user_info=Depends(user_permission.auth_seller_permissions)
):
    return user_info


@router.post('/buyer')
async def get_access_token(
    user_info=Depends(user_permission.auth_buyer_permissions)
):
    return user_info


@router.post('/all')
async def get_access_token(
    user_info=Depends(user_permission.auth_all_permissions)
):
    return user_info
