

from utils.db_vendors import Vendor, VENDOR_POSTGRESQL
from pydantic_settings import BaseSettings, SettingsConfigDict
from utils.enums.environments import Environment
from pydantic import computed_field

class MainDB:
    class Development(BaseSettings):
        model_config = SettingsConfigDict(env_file='.env',
                                          env_prefix='FORUM_DB_',
                                          env_ignore_empty=True,
                                          extra="ignore")
        SERVER = "localhost"
        NAME = "main-dev"
        PORT: int | None = None
        USER: str | None = None
        PASSWORD: str | None = None
        VENDOR: Vendor = VENDOR_POSTGRESQL
        ENVIRONMENT: Environment = Environment.DEVELOPMENT
        
        @computed_field
        @property
        def URI(self) -> str:
            uri = self.VENDOR.generate_uri(self.USER, self.PASSWORD, self.SERVER, self.PORT, self.NAME)
            return uri

        @computed_field
        @property
        def ASYNC_URI(self) -> str:
            uri = self.VENDOR.generate_async_uri(self.USER, self.PASSWORD, self.SERVER, self.PORT, self.NAME)
            return uri
    
    class Production(BaseSettings):
        model_config = SettingsConfigDict(env_file='.env',
                                          env_prefix='FORUM_DB_',
                                          env_ignore_empty=True,
                                          extra="ignore")
        SERVER: str = "localhost"
        NAME: str = r"main-prod"
        PORT: int | None = None
        USER: str | None = None
        PASSWORD: str | None = None
        VENDOR: Vendor = VENDOR_POSTGRESQL
        ENVIRONMENT: Environment = Environment.PRODUCTION
        
        @computed_field
        @property
        def URI(self) -> str:
            uri = self.VENDOR.generate_uri(self.USER, self.PASSWORD, self.SERVER, self.PORT, self.NAME)
            return uri

        @computed_field
        @property
        def ASYNC_URI(self) -> str:
            uri = self.VENDOR.generate_async_uri(self.USER, self.PASSWORD, self.SERVER, self.PORT, self.NAME)
            return uri

