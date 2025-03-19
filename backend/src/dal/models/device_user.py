from dal.models._base import Common
from sqlalchemy.orm import Mapped, mapped_column
from api.main.security.encrypted_column import Encrypted

class DeviceUser(Common):
    __tablename__ = 'user'
    
    name: Mapped[str]
    password: Mapped[str] = mapped_column(Encrypted(str))
