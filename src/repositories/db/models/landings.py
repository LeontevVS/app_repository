from sqlalchemy.orm import Mapped, mapped_column

from repositories.db.models.base_model import ORMBaseModel


class LandingModel(ORMBaseModel):
    __tablename__ = 'landings'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    canonical: Mapped[str]
    path: Mapped[str]
    update_time: Mapped[float]
    active: Mapped[bool]
    confirmed: Mapped[bool]
    title: Mapped[str]
    description: Mapped[str]
    redirect_authenticate: Mapped[bool]
    chatra: Mapped[bool]
    archived: Mapped[bool]
