from api.main.types._generic import GenericPublic, GenericPrivate, GenericFullInput, GenericPartialInput
from api.main.types.metadata import Metadata 
from pydantic import BaseModel
from uuid import UUID

class UserPublic(BaseModel, GenericPublic):
    id: UUID
    name: str
    admin: bool
    
class UserPrivate(Metadata, GenericPrivate):
    #is_deleted: bool
    id: UUID
    name: str
    password: str
    admin: bool
    
class UserFullInput(BaseModel, GenericFullInput):
    name: str
    password: str
    admin: bool
    
class UserPartialInput(BaseModel, GenericPartialInput):
    name: str | None
    password: str | None
    admin: bool | None