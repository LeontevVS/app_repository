from pydantic import BaseModel

from modules.users.consts import PublicUserRoles


class EmailSignInViewModel(BaseModel):
    email: str
    password: bytes
    role: PublicUserRoles


class EmailLogInViewModel(BaseModel):
    email: str
    password: bytes


class AccessTokenOutViewModel(BaseModel):
    token: str
    type: str = "Bearer"
