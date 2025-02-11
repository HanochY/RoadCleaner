from pydantic import BaseModel, AnyHttpUrl, IPvAnyAddress
from utils.enums.http_methods import HttpMethod
from uuid import UUID, uuid4

class RequestLog(BaseModel):
    req_id: UUID = uuid4()
    method: HttpMethod
    route: str
    ip: IPvAnyAddress
    url: AnyHttpUrl
    host: str | None
    body: str
    headers: dict

            