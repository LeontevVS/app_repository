from fastapi import (
    APIRouter,
    Depends,
)

from depends.auth_users import user_permission


router = APIRouter(tags=['test'], prefix='/test')


@router.get('/all_roles/')
async def test_all_roles(
    user_info=Depends(user_permission.auth_all_permissions)
):
    return user_info


@router.get('/admin_roles/')
async def test_admin_roles(
    user_info=Depends(user_permission.auth_admin_permissions)
):
    return user_info


@router.get('/seller_roles/')
async def test_seller_roles(
    user_info=Depends(user_permission.auth_seller_permissions)
):
    return user_info


@router.get('/buyer_roles/')
async def test_buyer_roles(
    user_info=Depends(user_permission.auth_buyer_permissions)
):
    return user_info
