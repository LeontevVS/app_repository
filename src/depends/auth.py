from depends.redis_connector import redis_pool
from services.auth.auth import AuthService
from services.auth.repositories.auth_repository import AuthRepository


# repositories
auth_repository = AuthRepository(redis_pool)

# services
auth_service = AuthService(
    auth_repository=auth_repository,
)


def get_auth_service() -> AuthService:
    return auth_service
