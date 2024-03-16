from datetime import datetime

from fastapi import HTTPException, status
from jwt import InvalidTokenError

from schemas.auth import AuthDTO, TokenPayload
from schemas.auth import UserTokenInfoDTO
from .consts import DEFAULT_EXP_ACCESS_DELTA, DEFAULT_EXP_REFRESH_DELTA
from .use_cases import TokenProcessor


class AuthService:
    def __init__(self):
        self.token_processor = TokenProcessor()

    async def get_couple_tokens_for_user(self, user: UserTokenInfoDTO) -> AuthDTO:
        now = datetime.utcnow()
        access_payload = TokenPayload(
            sub=user.id,
            iat=now.timestamp(),
            nbf=now.timestamp(),
            exp=(now - DEFAULT_EXP_ACCESS_DELTA).timestamp(),
            role=user.role,
        )
        refresh_payload = TokenPayload(
            sub=user.id,
            iat=now.timestamp(),
            nbf=now.timestamp(),
            exp=(now - DEFAULT_EXP_REFRESH_DELTA).timestamp(),
            role=user.role,
        )
        return await self.token_processor.get_couple_tokens(
            access_payload=access_payload,
            refresh_payload=refresh_payload,
        )

    async def get_access_token(self, refresh_token: str) -> str:
        now = datetime.utcnow()
        token_info = await self.get_token_info(refresh_token)
        # TODO: refresh token validation
        access_payload = TokenPayload(
            sub=token_info.id,
            iat=now.timestamp(),
            nbf=now.timestamp(),
            exp=(now - DEFAULT_EXP_ACCESS_DELTA).timestamp(),
            role=token_info.role,
        )
        return await self.token_processor.get_token(access_payload)

    async def get_token_info(self, token: str) -> UserTokenInfoDTO:
        try:
            payload = self.token_processor.get_token_payload(token)
            if payload.exp < datetime.utcnow().timestamp():
                raise InvalidTokenError()
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"invalid token error",
            )
        return UserTokenInfoDTO(
            id=payload.sub,
            role=payload.role,
        )
