from services.users import UserService


# repositories

# services
user_service = UserService()


def get_user_service() -> UserService:
    return user_service
