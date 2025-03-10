from dal.models._base import Common
from sqlalchemy.orm import Mapped, relationship, mapped_column
from uuid import uuid4, UUID
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID

class DeviceType(Common):
    __tablename__ = 'device_type'

    name: Mapped[str]
    devices: Mapped[list["Device"]] = relationship(back_populates="type") # type: ignore
