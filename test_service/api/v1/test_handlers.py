from fastapi import (
    APIRouter,
    Request,
)


router = APIRouter(tags=['test'], prefix='/test')


@router.get('/all_roles/')
async def test_admin_roles(request: Request):
    return {'status': 'ok', 'headers': request.headers.items()}


@router.get('/admin_roles/')
async def test_admin_roles(request: Request):
    return {'status': 'ok', 'headers': request.headers.items()}


@router.get('/seller_roles/')
async def test_admin_roles(request: Request):
    return {'status': 'ok', 'headers': request.headers.items()}


@router.get('/buyer_roles/')
async def test_admin_roles(request: Request):
    return {'status': 'ok', 'headers': request.headers.items()}
