from pydantic import BaseModel


class LandingDTO(BaseModel):
    id: int
    name: str
    canonical: str
    path: str
    update_time: float
    active: bool
    confirmed: bool
    title: str
    description: str
    redirect_authenticate: bool
    chatra: bool
    archived: bool
