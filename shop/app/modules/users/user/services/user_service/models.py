from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from modules.users.consts import PrivateUserRoles


class CreationUserDTO(BaseModel):
    role: PrivateUserRoles


class UserInfoDTO(BaseModel):
    user_id: UUID
    role: PrivateUserRoles
    deleted: bool = False
    created_at: datetime
    deleted_at: datetime | None = None
