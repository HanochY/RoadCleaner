from dal.models._base import Common
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, CheckConstraint
from uuid import uuid4, UUID
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID

class Interface(Common):
    __tablename__ = 'interface'
    
    id: Mapped[UUID] = mapped_column(SQL_UUID(as_uuid=True), default=uuid4, primary_key=True)
    name: Mapped[str]
    ip: Mapped[str]
    device_id: Mapped[UUID] = mapped_column(ForeignKey("device.id"), name="device")
    tunnel_core_of_id: Mapped[UUID | None] = mapped_column(ForeignKey("tunnel.id"), name="tunnel_core_of", unique=True, default=None)
    tunnel_edge_of_id: Mapped[UUID | None] = mapped_column(ForeignKey("tunnel.id"), name="tunnel_edge_of", unique=True, default=None)
    
    device: Mapped["Device"] = relationship(back_populates="interfaces") # type: ignore

    __table_args__ = (
        CheckConstraint(
            '(tunnel_core_of IS NULL OR tunnel_edge_of IS NULL)',
            name='check_interfaces_not_both_none'
        ),
    )
