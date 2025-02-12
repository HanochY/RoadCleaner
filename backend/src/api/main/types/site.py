from api.main.types._generic import GenericPublic, GenericPrivate, GenericFullInput, GenericPartialInput
from pydantic import BaseModel
from uuid import UUID

class SitePublic(BaseModel, GenericPublic):
    id: UUID
    name: str
    
class SitePrivate(BaseModel, GenericPrivate):
    id: UUID
    name: str
    
class SiteFullInput(BaseModel, GenericFullInput):
    name: str

class SitePartialInput(BaseModel, GenericPartialInput):
    name: str | None