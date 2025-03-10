from api.main.types._generic import GenericPublic, GenericPrivate, GenericFullInput, GenericPartialInput
from api.main.types.metadata import Metadata 
from pydantic import BaseModel
from uuid import UUID

class SitePublic(BaseModel, GenericPublic):
    id: UUID
    name: str
    
class SitePrivate(Metadata, GenericPrivate):
    id: UUID
    name: str
    
class SiteFullInput(BaseModel, GenericFullInput):
    name: str
    class Config(GenericFullInput.Config):
        pass
class SitePartialInput(BaseModel, GenericPartialInput):
    name: str | None = None
    class Config(GenericPartialInput.Config):
        pass