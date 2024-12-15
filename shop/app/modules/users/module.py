from fastapi import APIRouter

from modules.users.user_access._handlers.email_access import email_router
from modules.users.user_access._handlers.logout import logout_router
from modules.users.auth._handlers.token_handlers import token_router


def _get_v1_router() -> APIRouter:
    v1_router = APIRouter(prefix="/api/v1")
    v1_router.include_router(email_router)
    v1_router.include_router(logout_router)
    v1_router.include_router(token_router)
    return v1_router


def get_module_router() -> APIRouter:
    module_router = APIRouter(tags=["users"], prefix="/users")
    module_router.include_router(_get_v1_router())
    return module_router
