
import json
from typing import Annotated

from pydantic import AnyUrl, field_validator, Field
from pydantic_settings import BaseSettings

from utils.enums.environments import Environment

class AppSettings(BaseSettings):
    ENVIRONMENT: Annotated[Environment, Field(validate_default=True)]
    ADDRESS: str
    PORT: int
    TRACK_MODIFICATIONS: bool
    DEBUG: bool
    ALLOWED_ORIGINS: list[AnyUrl]
    THREAD_COUNT: int
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ACCESS_TOKEN_ALGORITHM: str
    
    @field_validator('ENVIRONMENT', mode="before")
    @classmethod
    def str_to_environment(cls, v: str) -> Environment:
        return Environment(v.upper())
    
    @field_validator('ALLOWED_ORIGINS', mode="before")
    @classmethod
    def str_to_url_list(cls, v: str | list[AnyUrl]) -> list[AnyUrl]:
        if isinstance(v, str):
            return json.loads(v)
        else:
            return v
    
    @field_validator('ALLOWED_ORIGINS', mode="after")
    @classmethod
    def strip_urls(cls, v: list[AnyUrl]) -> list[AnyUrl]:
        return [AnyUrl(str(i).strip("/")) for i in v]
