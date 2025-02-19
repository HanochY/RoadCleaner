from pydantic import BaseModel 
from datetime import datetime 
from uuid import UUID

class Metadata(BaseModel):
    is_deleted: bool 
    created_at: datetime
    created_by: UUID
    modified_at: datetime
    modified_by: UUID
    deleted_at: datetime | None
    deleted_by: UUID | None