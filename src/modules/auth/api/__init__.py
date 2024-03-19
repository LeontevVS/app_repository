from fastapi import APIRouter

from . import v1

router = APIRouter(prefix='/v1')
router.include_router(v1.router)
