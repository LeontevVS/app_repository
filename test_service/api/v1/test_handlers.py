from fastapi import (
    APIRouter,
)


router = APIRouter(tags=['test'], prefix='/test')


@router.get('/all_roles/')
async def test_admin_roles():
    return {'status': 'ok'}


@router.get('/admin_roles/')
async def test_admin_roles():
    return {'status': 'ok'}


@router.get('/seller_roles/')
async def test_admin_roles():
    return {'status': 'ok'}


@router.get('/buyer_roles/')
async def test_admin_roles():
    return {'status': 'ok'}
