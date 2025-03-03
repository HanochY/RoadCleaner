from api.main.types._generic import GenericPublic, GenericPrivate, GenericFullInput, GenericPartialInput
from api.main.types.metadata import Metadata 
from pydantic import BaseModel
from uuid import UUID

class DeviceTypePublic(BaseModel, GenericPublic):
    id: UUID
    name: str
    
class DeviceTypePrivate(Metadata, GenericPrivate):
    id: UUID
    name: str
    
class DeviceTypeFullInput(BaseModel, GenericFullInput):
    name: str

class DeviceTypePartialInput(BaseModel, GenericPartialInput):
    name: str | None = None