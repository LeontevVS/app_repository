import jwt

from schemas.auth import AuthDTO, TokenPayload
from src.config import settings


class TokenProcessor:
    async def get_couple_tokens(
        self,
        access_payload: TokenPayload,
        refresh_payload: TokenPayload,
    ) -> AuthDTO:
        access_token = await self.get_token(access_payload)
        refresh_token = await self.get_token(refresh_payload)
        # TODO savin actual refresh token
        return AuthDTO(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def get_token(self, payload: TokenPayload) -> str:
        return self._encode_jwt(payload)

    @staticmethod
    def _encode_jwt(
        payload: TokenPayload,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
    ) -> str:
        encoded = jwt.encode(
            payload.model_dump(),
            private_key,
            algorithm=algorithm,
        )
        return encoded

    @staticmethod
    def get_token_payload(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
    ) -> TokenPayload:
        decoded = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
        )
        return TokenPayload(**decoded)
