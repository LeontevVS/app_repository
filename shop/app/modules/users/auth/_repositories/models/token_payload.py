from pydantic import BaseModel

from modules.users.consts import PrivateUserRoles


class TokenPayloadDTO(BaseModel):
    sub: str
    iat: float
    nbf: float
    exp: float
    role: PrivateUserRoles
