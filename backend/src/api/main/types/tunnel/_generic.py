from api.main.types._generic import GenericPublic, GenericPrivate, GenericFullInput, GenericPartialInput
from api.main.types.metadata import Metadata 
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class TunnelPublic(BaseModel, GenericPublic):
    id: UUID
    name: str
    interface_core_id: UUID 
    interface_edge_id: UUID 
    reinforced_at: datetime | None = None
    reinforced_by: str | None = None
    
class TunnelPrivate(Metadata, GenericPrivate):
    id: UUID
    name: str
    interface_core_id: UUID 
    interface_edge_id: UUID 
    reinforced_at: datetime | None = None
    reinforced_by: str | None = None
    
class TunnelFullInput(BaseModel, GenericFullInput):
    name: str
    interface_core_id: UUID 
    interface_edge_id: UUID
    class Config(GenericFullInput.Config):
        pass

class TunnelPartialInput(BaseModel, GenericPartialInput):
    id: UUID | None = None
    name: str | None = None
    interface_core_id: UUID | None = None
    interface_edge_id: UUID | None = None
    class Config(GenericPartialInput.Config):
        pass
