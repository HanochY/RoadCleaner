from api.main.types._generic import GenericPublic, GenericPrivate, GenericFullInput, GenericPartialInput
from api.main.types.metadata import Metadata 
from pydantic import BaseModel
from uuid import UUID

class DeviceUserPublic(BaseModel, GenericPublic):
    id: UUID
    name: str
    
class DeviceUserPrivate(Metadata, GenericPrivate):
    id: UUID
    name: str
    password: str
    
class DeviceUserFullInput(BaseModel, GenericFullInput):
    name: str
    password: str
    class Config(GenericFullInput.Config):
        pass
class DeviceUserPartialInput(BaseModel, GenericPartialInput):
    name: str | None = None
    password: str | None = None
    class Config(GenericPartialInput.Config):
        pass