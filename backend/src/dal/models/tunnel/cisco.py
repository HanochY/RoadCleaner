from dal.models.tunnel._base import Tunnel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from uuid import UUID

class CiscoTunnel(Tunnel):
    __tablename__ = 'cisco_tunnel_details'
    
    id: Mapped[UUID] = mapped_column(ForeignKey("tunnel.id"), primary_key=True)
    keychain_core: Mapped[str]
    keychain_edge: Mapped[str]
    key_name_core: Mapped[str]
    key_name_edge: Mapped[str]
    __mapper_args__ = {
        'polymorphic_identity': 'cisco_tunnel'
    }