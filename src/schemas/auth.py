from pydantic import BaseModel

from enums.user_enums import PrivateUserRoles


class TokenPayload(BaseModel):
    sub: str
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
