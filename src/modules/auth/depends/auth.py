from src.modules.auth.depends.redis_connector import redis_pool
from src.modules.auth.services.auth import AuthService
from src.modules.auth.repositories.redis_cache.auth_repository import AuthRepository


# repositories
auth_repository = AuthRepository(redis_pool)

# services
auth_service = AuthService(
    auth_repository=auth_repository,
)


def get_auth_service() -> AuthService:
    return auth_service
