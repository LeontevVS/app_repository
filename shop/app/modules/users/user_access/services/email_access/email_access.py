import random
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
from .exc import EmailAccessAlreadyExistsError, IncorrectLoginDataError
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
from modules.users.user_access._repositories.email_access_cache import (
    EmailAccessCacheP,
    get_email_access_cache,
    UnconfirmedEmailSignIn,
)


class EmailUserAccessService(EmailUserAccessServiceP):
    def __init__(
        self,
        user_service: UserServiceP,
        auth_service: TokenServiceP,
        email_access_repo: EmailAccessRepositoryP,
        email_access_cache: EmailAccessCacheP,
        password_cryptographer: PasswordCryptographerP
    ):
        self._user_service = user_service
        self._auth_service = auth_service
        self._email_access_repo = email_access_repo
        self._email_access_cache = email_access_cache
        self._password_cryptographer = password_cryptographer

    async def login_with_password(self, email: str, password: bytes) -> CoupleTokensDTO | None:
        async with self._email_access_repo:
            email_access = await self._email_access_repo.get_email_access(email=email)
            if not email_access:
                raise IncorrectLoginDataError()
            password_salt: bytes = cast(bytes, email_access.password_salt)
            hashed_input_password = await self._password_cryptographer.encrypt_password(
                password=password,
                salt=password_salt,
            )
            if email_access.hashed_password != hashed_input_password:
                IncorrectLoginDataError()
            user_id: UUID = cast(UUID, email_access.user_id)
            user = await self._user_service.get_user(user_id=user_id)
            if user.deleted:
                raise IncorrectLoginDataError()
            return await self._auth_service.generate_couple_tokens_for_user(
                user_info=TokenUserInfoDTO(
                    user_id=user.user_id,
                    role=user.role,
                )
            )

    async def signin_with_password(self, email: str, password: bytes, role: PublicUserRoles) -> int:
        async with self._email_access_cache:
            unconfirmed_registration = await self._email_access_cache.get_unconfirmed_email_signin(email=email)
            if unconfirmed_registration:
                raise Exception()
            code = random.randint(100000, 999999)
            await self._email_access_cache.add_unconfirmed_email_signin(
                data=UnconfirmedEmailSignIn(
                    email=email,
                    password=str(password),
                    role=PrivateUserRoles(role),
                    code=code,
                )
            )
        return code

    async def confirm_email(self, email: str, code: str) -> CoupleTokensDTO:
        async with self._email_access_cache:
            unconfirmed_registration = await self._email_access_cache.get_unconfirmed_email_signin(email=email)
        if code != unconfirmed_registration.secret_code:
            raise Exception()
        async with self._email_access_repo:
            existing_email_access = await self._email_access_repo.get_email_access(email=email)
            if existing_email_access:
                raise EmailAccessAlreadyExistsError()
            new_user_id = await self._user_service.create_user(
                creation_data=CreationUserDTO(role=PrivateUserRoles(unconfirmed_registration.role))
            )
            salt = await self._password_cryptographer.generate_salt()
            hashed_password = await self._password_cryptographer.encrypt_password(
                password=unconfirmed_registration.password.encode(),
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
                role=unconfirmed_registration.role,
            )
        )


def get_email_user_access_service() -> EmailUserAccessServiceP:
    return EmailUserAccessService(
        user_service=get_user_service(),
        auth_service=get_token_service(),
        email_access_repo=get_email_access_repository(),
        email_access_cache=get_email_access_cache(),
        password_cryptographer=get_password_cryptographer(),
    )
