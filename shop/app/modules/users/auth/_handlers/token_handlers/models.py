from pydantic import BaseModel


class AccessTokenOutViewModel(BaseModel):
    token: str
    type: str = "Bearer"
