from dal.models._base import Common
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4, UUID
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID

class Device(Common):
    __tablename__ = 'device'

    id: Mapped[SQL_UUID] = mapped_column(SQL_UUID(as_uuid=True), default=uuid4, primary_key=True)
    name: Mapped[str]
    ip: Mapped[str]
    type_id: Mapped[SQL_UUID] = mapped_column(ForeignKey("device_type.id"), name="type")
    site_id: Mapped[SQL_UUID] = mapped_column(ForeignKey("site.id"), name="site")
    
    type: Mapped["DeviceType"] = relationship(back_populates="devices") # type: ignore
    site: Mapped["Site"] = relationship(back_populates="devices") # type: ignore
    interfaces: Mapped[list["Interface"]] = relationship(back_populates="device") # type: ignore