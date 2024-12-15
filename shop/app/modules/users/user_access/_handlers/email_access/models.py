from pydantic import BaseModel

from modules.users.consts import PublicUserRoles


class EmailSignInViewModel(BaseModel):
    email: str
    password: str
    role: PublicUserRoles


class EmailLogInViewModel(BaseModel):
    email: str
    password: str


class AccessTokenOutViewModel(BaseModel):
    token: str
    type: str = "Bearer"
