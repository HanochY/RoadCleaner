from dal.schema.resources._generic import GenericPublic, GenericPrivate, GenericFullInput, GenericPartialInput
from pydantic import BaseModel
from uuid import UUID


class TopicPublic(BaseModel, GenericPublic):
    uid: UUID
    name: str
    id: UUID
class TopicPrivate(BaseModel, GenericPrivate):
    uid: UUID
    name: str
    id: UUID
class TopicFullInput(BaseModel, GenericFullInput):
    uid: UUID
    name: str
class TopicPartialInput(BaseModel, GenericPartialInput):
    uid: UUID | None
    name: str | None
