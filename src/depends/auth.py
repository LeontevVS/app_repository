from services.auth.auth import AuthService


# repositories

# services
auth_service = AuthService()


def get_auth_service() -> AuthService:
    return auth_service
