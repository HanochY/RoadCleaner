from dal.models._base import Common
#from dal.models.device import Device
from sqlalchemy.orm import Mapped, relationship

class Site(Common):
    __tablename__ = 'site'
    
    name: Mapped[str]
    devices: Mapped[list["Device"]] = relationship(back_populates="site")