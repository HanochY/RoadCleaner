from pydantic import BaseModel
from uuid import UUID, uuid4

class ErrorLog(BaseModel):
    req_id: UUID = uuid4()
    error_message: str