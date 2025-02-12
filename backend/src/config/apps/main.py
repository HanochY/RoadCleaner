import os
import secrets
from typing import Annotated
from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from utils.enums.environments import Environment
from config.apps._schema import AppSettings

class MainApp:
    class Development(AppSettings):
        model_config = SettingsConfigDict(env_file='.env',
                                          env_prefix='MAIN_APP_DEV',
                                          env_ignore_empty=True,
                                          extra="ignore")
        ENVIRONMENT: Annotated[Environment, Field(validate_default=True)] = Environment.DEVELOPMENT
        ADDRESS: str = "localhost"
        PORT: int = 5000
        TRACK_MODIFICATIONS: bool = True
        DEBUG: bool = True
        ALLOWED_ORIGINS: list[AnyUrl] = ["http://localhost", "http://localhost:5173", "https://localhost", "https://localhost:5173"]
        THREAD_COUNT: int = 1
        SECRET_KEY: str = secrets.token_urlsafe(32)
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 7200 # 5 Days
        ACCESS_TOKEN_ALGORITHM: str = "HS256"


    class Production(AppSettings):
        model_config = SettingsConfigDict(env_file='.env',
                                          env_prefix='MAIN_APP_PROD_',
                                          env_ignore_empty=True,
                                          extra="ignore")
        ENVIRONMENT: Annotated[Environment, Field(validate_default=True)] = Environment.PRODUCTION
        ADDRESS: str = "0.0.0.0"
        PORT: int = 80
        TRACK_MODIFICATIONS: bool = False
        DEBUG: bool = False
        THREAD_COUNT: int = os.cpu_count() * 2 + 1
        SECRET_KEY: str = secrets.token_urlsafe(32)
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
        ACCESS_TOKEN_ALGORITHM: str = "HS256"