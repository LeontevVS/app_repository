import jwt

from .proto import TokenProcessorP
from modules.users.auth._repositories.models.token_payload import TokenPayloadDTO
from modules.users.settings import SETTINGS


class TokenProcessor(TokenProcessorP):
    def __init__(self, private_key: str, public_key: str, algorithm: str) -> None:
        self._private_key = private_key
        self._public_key = public_key
        self._algorithm = algorithm

    def generate_token(self, payload: TokenPayloadDTO) -> str:
        encoded = jwt.encode(
            payload=payload.model_dump(),
            key=self._private_key,
            algorithm=self._algorithm,
        )
        return encoded

    def get_token_payload(self, token: str) -> TokenPayloadDTO:
        decoded = jwt.decode(
            jwt=token,
            key=self._public_key,
            algorithms=[self._algorithm],
        )
        return TokenPayloadDTO.model_validate(obj=decoded, from_attributes=True)

    def get_expired_token_payload(self, token: str) -> TokenPayloadDTO:
        decoded = jwt.decode(
            jwt=token,
            key=self._public_key,
            algorithms=[self._algorithm],
            options={
                "verify_exp": False,
            }
        )
        return TokenPayloadDTO.model_validate(obj=decoded, from_attributes=True)


def get_token_processor() -> TokenProcessor:
    return TokenProcessor(
        private_key=SETTINGS.auth_jwt.private_key_path.read_text(),
        public_key=SETTINGS.auth_jwt.public_key_path.read_text(),
        algorithm=SETTINGS.auth_jwt.algorithm,
    )
