from pydantic import BaseModel 
from datetime import datetime 

class Metadata(BaseModel):
    is_deleted: bool 
    created_at: datetime
    created_by: str
    modified_at: datetime
    modified_by: str
    deleted_at: datetime | None
    deleted_by: str | None