from pydantic import BaseModel

from modules.users.consts import PrivateUserRoles


class UnconfirmedEmailSignIn(BaseModel):
    email: str
    password: str
    role: PrivateUserRoles
    code: int
