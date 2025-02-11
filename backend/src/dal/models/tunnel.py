from dal.models._base import Common
from dal.models.interface import Interface
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import ForeignKey
from uuid import UUID

class Tunnel(Common):
    name: Mapped[str]
    interfaces: Mapped[list[Interface]] = relationship(back_populates="device")
