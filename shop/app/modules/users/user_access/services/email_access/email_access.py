from typing import cast
from uuid import UUID

from modules.users.auth.services.token_service import (
    TokenServiceP,
    CoupleTokensDTO,
    get_token_service,
    TokenUserInfoDTO,
)
from modules.users.consts import PublicUserRoles, PrivateUserRoles
from modules.users.user.services.user_service import UserServiceP, CreationUserDTO, get_user_service
from .proto import EmailUserAccessServiceP
from modules.users.user_access._repositories.email_access_repository import (
    EmailAccessRepositoryP,
    EmailAccessTableModel,
    get_email_access_repository,
)
from modules.users.user_access._repositories.password_cryptographer import (
    PasswordCryptographerP,
    get_password_cryptographer,
)


class EmailUserAccessService(EmailUserAccessServiceP):
    def __init__(
        self,
        user_service: UserServiceP,
        auth_service: TokenServiceP,
        email_access_repo: EmailAccessRepositoryP,
        password_cryptographer: PasswordCryptographerP
    ):
        self._user_service = user_service
        self._auth_service = auth_service
        self._email_access_repo = email_access_repo
        self._password_cryptographer = password_cryptographer

    async def login_with_password(self, email: str, password: bytes) -> CoupleTokensDTO | None:
        async with self._email_access_repo:
            email_access = await self._email_access_repo.get_email_access(email=email)
            if not email_access:
                return
            password_salt: bytes = cast(bytes, email_access.password_salt)
            hashed_input_password = await self._password_cryptographer.encrypt_password(
                password=password,
                salt=password_salt,
            )
            if email_access.hashed_password != hashed_input_password:
                return
            user_id: UUID = cast(UUID, email_access.user_id)
            user = await self._user_service.get_user(user_id=user_id)
            return await self._auth_service.generate_couple_tokens_for_user(
                user_info=TokenUserInfoDTO(
                    user_id=user.user_id,
                    role=user.role,
                )
            )

    async def signin_with_password(self, email: str, password: bytes, role: PublicUserRoles) -> CoupleTokensDTO | None:
        async with self._email_access_repo:
            existing_email_access = await self._email_access_repo.get_email_access(email=email)
            if existing_email_access:
                return
            new_user_id = await self._user_service.create_user(
                creation_data=CreationUserDTO(role=PrivateUserRoles(role))
            )
            salt = await self._password_cryptographer.generate_salt()
            hashed_password = await self._password_cryptographer.encrypt_password(
                password=password,
                salt=salt,
            )
            email_access = EmailAccessTableModel(
                email=email,
                user_id=new_user_id,
                hashed_password=hashed_password,
                password_salt=salt,
            )
            await self._email_access_repo.create_email_access(data=email_access)

        return await self._auth_service.generate_couple_tokens_for_user(
            user_info=TokenUserInfoDTO(
                user_id=new_user_id,
                role=role,
            )
        )


def get_email_user_access_service() -> EmailUserAccessServiceP:
    return EmailUserAccessService(
        user_service=get_user_service(),
        auth_service=get_token_service(),
        email_access_repo=get_email_access_repository(),
        password_cryptographer=get_password_cryptographer(),
    )
