from api.main.types._generic import GenericPublic, GenericPrivate, GenericFullInput, GenericPartialInput
from api.main.types.metadata import Metadata 
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class TunnelPublic(BaseModel, GenericPublic):
    id: UUID
    name: str
    interface_inner_id: UUID 
    interface_outer_id: UUID 
    reinforced_at: datetime | None = None
    reinforced_by: str | None = None
    
class TunnelPrivate(Metadata, GenericPrivate):
    id: UUID
    name: str
    interface_inner_id: UUID 
    interface_outer_id: UUID 
    reinforced_at: datetime | None = None
    reinforced_by: str | None = None
    
class TunnelFullInput(BaseModel, GenericFullInput):
    name: str
    interface_inner_id: UUID 
    interface_outer_id: UUID
    class Config(GenericFullInput.Config):
        pass

class TunnelPartialInput(BaseModel, GenericPartialInput):
    name: str | None = None
    interface_inner_id: UUID | None = None
    interface_outer_id: UUID | None = None
    class Config(GenericPartialInput.Config):
        pass
