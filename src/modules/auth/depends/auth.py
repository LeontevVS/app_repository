from depends.redis_connector import redis_pool
from services.auth import AuthService
from repositories.redis_cache.auth_repository import AuthRepository


# repositories
auth_repository = AuthRepository(redis_pool)

# services
auth_service = AuthService(
    auth_repository=auth_repository,
)


def get_auth_service() -> AuthService:
    return auth_service
