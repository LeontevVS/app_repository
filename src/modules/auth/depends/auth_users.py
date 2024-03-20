from src.modules.auth.services.auth_users import AuthUserService, UserPermission
from .auth import auth_service
from .db_connector import async_session_maker
from .users import user_service


# repositories

# services
auth_user_service = AuthUserService(
    async_session_maker=async_session_maker,
    user_service=user_service,
    auth_service=auth_service,
)
user_permission = UserPermission(auth_user_service)


def get_auth_user_service() -> AuthUserService:
    return auth_user_service
