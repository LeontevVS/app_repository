from fastapi import APIRouter
from . import auth, users

router = APIRouter(prefix='/v1/auth')

router.include_router(auth.public_router)
router.include_router(auth.private_router)

router.include_router(users.public_router)
router.include_router(users.private_router)

