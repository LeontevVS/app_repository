import bcrypt

from schemas.users import UserSignInDTO, UserLogInDTO, ValidUser, UserToCreate


class UserService:
    def __init__(self):
        pass

    async def get_user_by_login_creds(self, user: UserLogInDTO) -> ValidUser:
        pass

    async def create_user(self, user: UserSignInDTO) -> ValidUser:
        user_to_create = UserToCreate(
            phone_number=user.phone_number,
            role: PublicUserRoles
            hashed_password: bytes
        )
        # TODO: check phone number
        pass

    @staticmethod
    def hash_password(
        password: str,
    ) -> bytes:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)

    @staticmethod
    def validate_password(
        password: str,
        hashed_password: bytes,
    ) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )
