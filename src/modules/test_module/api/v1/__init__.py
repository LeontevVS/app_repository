from fastapi import APIRouter
from . import (
    test_handlers,
)

router = APIRouter(prefix='/v1')
router.include_router(test_handlers.router)
