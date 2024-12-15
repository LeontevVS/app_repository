from datetime import datetime, timezone

from .consts import DEFAULT_EXP_ACCESS_DELTA, DEFAULT_EXP_REFRESH_DELTA
from .exc import RefreshTokenExpiredError
from .proto import TokenServiceP
from .models import CoupleTokensDTO, TokenUserInfoDTO
from modules.users.auth._repositories.models.token_payload import TokenPayloadDTO
from modules.users.auth._repositories.token_processor import TokenProcessorP, get_token_processor
from modules.users.auth._repositories.token_repository import TokenRepositoryP, get_token_repository


class TokenService(TokenServiceP):
    def __init__(self, token_processor: TokenProcessorP, token_repository: TokenRepositoryP) -> None:
        self._token_processor = token_processor
        self._token_repository = token_repository

    async def generate_couple_tokens_for_user(self, user_info: TokenUserInfoDTO) -> CoupleTokensDTO:
        now = datetime.now(tz=timezone.utc)
        access_payload = TokenPayloadDTO(
            sub=str(user_info.user_id),
            iat=now.timestamp(),
            nbf=now.timestamp(),
            exp=(now + DEFAULT_EXP_ACCESS_DELTA).timestamp(),
            role=user_info.role,
        )
        refresh_payload = TokenPayloadDTO(
            sub=str(user_info.user_id),
            iat=now.timestamp(),
            nbf=now.timestamp(),
            exp=(now + DEFAULT_EXP_REFRESH_DELTA).timestamp(),
            role=user_info.role,
        )
        couple_tokens = CoupleTokensDTO(
            access_token=self._token_processor.generate_token(payload=access_payload),
            refresh_token=self._token_processor.generate_token(payload=refresh_payload),
        )
        async with self._token_repository:
            await self._token_repository.set_cache_token(
                token=couple_tokens.refresh_token,
                token_payload=refresh_payload,
                exp=DEFAULT_EXP_REFRESH_DELTA,
            )
            await self._token_repository.add_client_session(
                user_id=str(user_info.user_id),
                token=couple_tokens.refresh_token,
            )
        return couple_tokens

    async def reissue_tokens(self, refresh_token: str) -> CoupleTokensDTO:
        old_token_payload = await self._get_refresh_token_if_exists(refresh_token=refresh_token)
        now = datetime.now(tz=timezone.utc)
        access_payload = TokenPayloadDTO(
            sub=old_token_payload.sub,
            iat=now.timestamp(),
            nbf=now.timestamp(),
            exp=(now + DEFAULT_EXP_ACCESS_DELTA).timestamp(),
            role=old_token_payload.role,
        )
        refresh_payload = TokenPayloadDTO(
            sub=old_token_payload.sub,
            iat=now.timestamp(),
            nbf=now.timestamp(),
            exp=(now + DEFAULT_EXP_REFRESH_DELTA).timestamp(),
            role=old_token_payload.role,
        )
        couple_tokens = CoupleTokensDTO(
            access_token=self._token_processor.generate_token(payload=access_payload),
            refresh_token=self._token_processor.generate_token(payload=refresh_payload),
        )
        async with self._token_repository:
            await self._token_repository.remove_token(token=refresh_token)
            await self._token_repository.remove_client_session(
                user_id=old_token_payload.sub,
                token=refresh_token,
            )
            await self._token_repository.set_cache_token(
                token=couple_tokens.refresh_token,
                token_payload=refresh_payload,
                exp=DEFAULT_EXP_REFRESH_DELTA,
            )
            await self._token_repository.add_client_session(
                user_id=old_token_payload.sub,
                token=couple_tokens.refresh_token,
            )
        return couple_tokens

    async def remove_refresh_token(self, refresh_token: str) -> None:
        async with self._token_repository:
            await self._token_repository.remove_token(token=refresh_token)
            token_payload = self._token_processor.get_expired_token_payload(token=refresh_token)
            await self._token_repository.remove_client_session(user_id=token_payload.sub, token=refresh_token)

    async def generate_access_token_from_refresh(self, refresh_token: str) -> str:
        refresh_token_info = await self._get_refresh_token_if_exists(refresh_token=refresh_token)
        now = datetime.now(tz=timezone.utc)
        access_payload = TokenPayloadDTO(
            sub=str(refresh_token_info.sub),
            iat=now.timestamp(),
            nbf=now.timestamp(),
            exp=(now + DEFAULT_EXP_ACCESS_DELTA).timestamp(),
            role=refresh_token_info.role,
        )
        return self._token_processor.generate_token(access_payload)

    async def get_access_token_user_info(self, access_token: str) -> TokenUserInfoDTO:
        token_payload = self._token_processor.get_token_payload(token=access_token)
        return TokenUserInfoDTO(
            user_id=token_payload.sub,
            role=token_payload.role,
        )

    async def _get_refresh_token_if_exists(self, refresh_token: str) -> TokenPayloadDTO:
        async with self._token_repository:
            refresh_token_info = await self._token_repository.get_refresh_token_info(token=refresh_token)
            if not refresh_token_info:
                token_payload = self._token_processor.get_expired_token_payload(token=refresh_token)
                await self._token_repository.remove_client_session(
                    user_id=token_payload.sub,
                    token=refresh_token,
                )
                raise RefreshTokenExpiredError()
        return refresh_token_info


def get_token_service() -> TokenService:
    return TokenService(
        token_processor=get_token_processor(),
        token_repository=get_token_repository(),
    )
