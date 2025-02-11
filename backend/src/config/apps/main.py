import os
import secrets
from typing import Annotated
import json
from pydantic import AnyUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from utils.enums.environments import Environment


class AppSettings(BaseSettings):
    pass

class MainApp:
    class Development(AppSettings):
        model_config = SettingsConfigDict(env_file='.env',
                                          env_prefix='FORUM_BACKEND_',
                                          env_ignore_empty=True,
                                          extra="ignore")
        ENVIRONEMT: Annotated[Environment, Field(validate_default=True)] = Environment.DEVELOPMENT
        ADDRESS: str = "localhost"
        PORT: int = 5000
        TRACK_MODIFICATIONS: bool = True
        DEBUG: bool = True
        ALLOWED_ORIGINS: list[AnyUrl] = ["http://localhost", "http://localhost:5173", "https://localhost", "https://localhost:5173"]
        THREAD_COUNT: int = 1
        SECRET_KEY: str = secrets.token_urlsafe(32)
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 7200 # 5 Days
        ACCESS_TOKEN_ALGORITHM: str = "HS256"
        
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

    class Production(AppSettings):
        model_config = SettingsConfigDict(env_file='.env',
                                          env_prefix='FORUM_BACKEND_',
                                          env_ignore_empty=True,
                                          extra="ignore")
        ENVIRONEMT: Annotated[Environment, Field(validate_default=True)] = Environment.PRODUCTION
        ADDRESS: str = "0.0.0.0"
        PORT: int = 80
        TRACK_MODIFICATIONS: bool = False
        DEBUG: bool = False
        THREAD_COUNT: int = os.cpu_count() * 2 + 1
        SECRET_KEY: str = secrets.token_urlsafe(32)
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
        ACCESS_TOKEN_ALGORITHM: str = "HS256"
        
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
