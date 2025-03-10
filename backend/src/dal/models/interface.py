from dal.models._base import Common
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, CheckConstraint
from uuid import uuid4, UUID
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID

class Interface(Common):
    __tablename__ = 'interface'
    
    name: Mapped[str]
    ip: Mapped[str]
    device_id: Mapped[UUID] = mapped_column(ForeignKey("device.id", ondelete="CASCADE"), name="device")
    tunnel_id: Mapped[UUID | None] = mapped_column(ForeignKey("tunnel.id"), name="tunnel", default=None)
    
    device: Mapped["Device"] = relationship(back_populates="interfaces") # type: ignore
