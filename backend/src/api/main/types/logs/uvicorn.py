from pydantic import BaseModel, AnyHttpUrl, IPvAnyAddress
from utils.enums.http_methods import HttpMethod

class UvicornLog(BaseModel):   
    client_addr: IPvAnyAddress
    method: HttpMethod
    full_path: AnyHttpUrl
    http_version: str
    status_code: int