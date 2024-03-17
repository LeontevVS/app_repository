from depends.db_connector import async_session_maker
from services.users import UserService
from repositories.users import UserRepository


# repositories
user_repository = UserRepository()

# services
user_service = UserService(
    async_session_maker=async_session_maker,
    user_repository=user_repository,
)


def get_user_service() -> UserService:
    return user_service
