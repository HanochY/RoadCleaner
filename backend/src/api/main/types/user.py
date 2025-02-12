from api.main.types._generic import GenericPublic, GenericPrivate, GenericFullInput, GenericPartialInput
from pydantic import BaseModel
from uuid import UUID

class UserPublic(BaseModel, GenericPublic):
    id: UUID
    name: str
    
class UserPrivate(BaseModel, GenericPrivate):
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