from uuid import UUID

from pydantic import BaseModel

from modules.users.consts import PrivateUserRoles


class CoupleTokensDTO(BaseModel):
    access_token: str
    refresh_token: str


class TokenUserInfoDTO(BaseModel):
    user_id: UUID
    role: PrivateUserRoles
