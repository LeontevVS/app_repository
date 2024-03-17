from depends.db_connector import get_async_session
from services.users import UserService
from repositories.users import UserRepository


# repositories
user_repository = UserRepository()

# services
user_service = UserService(
    get_session_maker=get_async_session,
    user_repository=user_repository,
)


def get_user_service() -> UserService:
    return user_service
