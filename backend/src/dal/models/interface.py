from dal.models._base import Common
from sqlalchemy.orm import Mapped, relationship
from dal.models.tunnel import Tunnel
from dal.models.device import Device
from sqlalchemy import ForeignKey
from uuid import UUID

class Interface(Common):
    name: Mapped[str]
    ip: Mapped[str]
    device_id: Mapped[UUID] = ForeignKey("device.id")
    tunnel_id: Mapped[UUID] = ForeignKey("tunnel.id")
    
    device: Mapped[Device] = relationship(back_populates="interfaces")
    tunnel: Mapped[Tunnel] = relationship(back_populates="interfaces")
