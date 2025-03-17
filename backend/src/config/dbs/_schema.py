from typing import Annotated
from pydantic import Field
from pydantic_settings import BaseSettings
from utils.db_vendors import Vendor
from utils.enums.environments import Environment
from pydantic import computed_field

class DBSettings(BaseSettings):
    ENVIRONMENT: Annotated[Environment, Field(validate_default=True)]
    SERVER: str
    NAME: str 
    PORT: int | None
    USER: str | None
    PASSWORD: str | None
    KEY: str | None
    VENDOR: Vendor
        
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