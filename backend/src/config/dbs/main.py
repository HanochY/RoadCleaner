

from utils.db_vendors import Vendor, VENDOR_POSTGRESQL
from pydantic_settings import BaseSettings, SettingsConfigDict
from utils.enums.environments import Environment
from pydantic import computed_field
from config.dbs._schema import DBSettings

class MainDB:
    class Development(DBSettings):
        model_config = SettingsConfigDict(env_file='.env',
                                          env_prefix='MAIN_DB_DEV_',
                                          env_ignore_empty=True,
                                          extra="ignore")
        SERVER: str = "localhost"
        NAME: str = "main-dev"
        PORT: int | None = 5432
        USER: str | None = "postgres"
        PASSWORD: str | None = "postgresking"
        VENDOR: Vendor = VENDOR_POSTGRESQL
        ENVIRONMENT: Environment = Environment.DEVELOPMENT

    class Production(BaseSettings):
        model_config = SettingsConfigDict(env_file='.env',
                                          env_prefix='MAIN_DB_PROD_',
                                          env_ignore_empty=True,
                                          extra="ignore")
        SERVER: str = "localhost"
        NAME: str = r"main-prod"
        PORT: int | None = None
        USER: str | None = None
        PASSWORD: str | None = None
        VENDOR: Vendor = VENDOR_POSTGRESQL
        ENVIRONMENT: Environment = Environment.PRODUCTION
