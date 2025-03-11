from dal.models._base import Common
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4, UUID
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID

class Device(Common):
    __tablename__ = 'device'

    name: Mapped[str]
    ip: Mapped[str]
    type: Mapped[UUID] = mapped_column(ForeignKey("device_type.name"), name="type")
    site_id: Mapped[UUID] = mapped_column(ForeignKey("site.id", ondelete="CASCADE"), name="site")
    
    site: Mapped["Site"] = relationship(back_populates="devices") # type: ignore
    interfaces: Mapped[list["Interface"]] = relationship(back_populates="device", cascade='all, delete') # type: ignore