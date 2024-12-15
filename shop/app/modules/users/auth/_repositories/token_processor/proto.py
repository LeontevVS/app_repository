from typing import Protocol

from modules.users.auth._repositories.models.token_payload import TokenPayloadDTO


class TokenProcessorP(Protocol):
    _private_key: str
    _public_key: str
    _algorithm: str

    def generate_token(self, payload: TokenPayloadDTO) -> str:
        pass

    def get_token_payload(self, token: str) -> TokenPayloadDTO:
        pass

    def get_expired_token_payload(self, token: str) -> TokenPayloadDTO:
        pass
