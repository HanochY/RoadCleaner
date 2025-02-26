from dal.models.tunnel._base import Tunnel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from uuid import UUID


class JuniperTunnel(Tunnel):
    __tablename__ = 'juniper_tunnel_details'
    
    id: Mapped[UUID] = mapped_column(ForeignKey("tunnel.id"), primary_key=True)
    associaton_name_core: Mapped[str]
    associaton_name_edge: Mapped[str]
    __mapper_args__ = {
        'polymorphic_identity': 'juniper_tunnel'
    }