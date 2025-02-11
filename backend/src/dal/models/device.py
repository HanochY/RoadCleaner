from dal.models._base import Common
#from dal.models.device_type import DeviceType
#from dal.models.site import Site
#from dal.models.interface import Interface
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from uuid import UUID

class Device(Common):
    __tablename__ = 'device'

    name: Mapped[str]
    ip: Mapped[str]
    type_id: Mapped[UUID] = ForeignKey("device_type.id")
    site_id: Mapped[UUID] = ForeignKey("site.id")
    
    type: Mapped["DeviceType"] = relationship(back_populates="devices")
    site: Mapped["Site"] = relationship(back_populates="devices")
    interfaces: Mapped[list["Interface"]] = relationship(back_populates="device")