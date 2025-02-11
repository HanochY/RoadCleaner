from dal.schema.resources._generic import GenericPublic, GenericPrivate, GenericFullInput, GenericPartialInput 
from pydantic import BaseModel
from uuid import UUID

class CommentPublic(BaseModel, GenericPublic):
    id: UUID
    uid: UUID
    title: str
    content: str
    topic_id: UUID
class CommentPrivate(BaseModel, GenericPrivate):
    id: UUID
    uid: UUID
    title: str
    content: str
    topic_id: UUID
class CommentFullInput(BaseModel, GenericFullInput):
    uid: UUID
    title: str
    content: str
    topic_id: UUID
class CommentPartialInput(BaseModel, GenericPartialInput):
    uid: UUID | None
    title: str | None
    content: str | None
    topic_id: UUID | None