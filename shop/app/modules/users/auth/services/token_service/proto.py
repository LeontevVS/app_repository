from typing import Protocol

from .models import CoupleTokensDTO, TokenUserInfoDTO
from modules.users.auth._repositories.token_processor import TokenProcessorP
from modules.users.auth._repositories.token_repository import TokenRepositoryP


class TokenServiceP(Protocol):
    _token_processor: TokenProcessorP
    _token_repository: TokenRepositoryP

    async def generate_couple_tokens_for_user(self, user_info: TokenUserInfoDTO) -> CoupleTokensDTO:
        pass

    async def reissue_tokens(self, refresh_token: str) -> CoupleTokensDTO:
        pass

    async def remove_refresh_token(self, refresh_token: str) -> None:
        pass

    async def generate_access_token_from_refresh(self, refresh_token: str) -> str:
        pass

    async def get_access_token_user_info(self, access_token: str) -> TokenUserInfoDTO:
        pass
