from fastapi import APIRouter
from . import (
    auth,
    users,
    test_handlers,
)

router = APIRouter(prefix='/api')
router.include_router(auth.router)
router.include_router(users.router)
router.include_router(test_handlers.router)
