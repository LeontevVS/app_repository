from pydantic import BaseModel

from enums.user_enums import PublicUserRoles, PrivateUserRoles


class UserSignInDTO(BaseModel):
    phone_number: str
    role: PublicUserRoles
    password: str


class UserLogInDTO(BaseModel):
    phone_number: str
    password: str


class ValidUser(BaseModel):
    id: int
    role: PrivateUserRoles


class UserToCreate(BaseModel):
    phone_number: str
    role: PrivateUserRoles
    hashed_password: bytes
