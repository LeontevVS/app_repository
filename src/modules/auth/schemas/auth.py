from pydantic import BaseModel

from src.modules.auth.enums.user_enums import PrivateUserRoles


class TokenPayload(BaseModel):
    sub: int
    iat: float
    nbf: float
    exp: float
    role: PrivateUserRoles


class AuthDTO(BaseModel):
    access_token: str
    refresh_token: str


class UserTokenInfoDTO(BaseModel):
    id: int
    role: PrivateUserRoles


class AuthenticatedUserDTO(BaseModel):
    id: int
    role: PrivateUserRoles
