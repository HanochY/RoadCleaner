from dal.models._base import Common
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from uuid import uuid4, UUID
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID

class Interface(Common):
    __tablename__ = 'interface'
    
    id: Mapped[SQL_UUID] = mapped_column(SQL_UUID(as_uuid=True), default=uuid4, primary_key=True)
    name: Mapped[str]
    ip: Mapped[str]
    device_id: Mapped[SQL_UUID] = mapped_column(ForeignKey("device.id"), name="device")
    tunnel_id: Mapped[SQL_UUID] = mapped_column(ForeignKey("tunnel.unique_name"), name="tunnel")
    
    device: Mapped["Device"] = relationship(back_populates="interfaces") # type: ignore
    tunnel: Mapped["Tunnel"] = relationship(back_populates="interfaces") # type: ignore
