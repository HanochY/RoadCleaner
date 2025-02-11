from typing import Annotated
from pydantic import Field
from pydantic_settings import BaseSettings
from utils.db_vendors import Vendor
from utils.enums.environments import Environment
from pydantic import computed_field

class DBSettings(BaseSettings):
    ENVIRONMENT: Annotated[Environment, Field(validate_default=True)]
    VENDOR: Annotated[Vendor, Field(validate_default=True)]
    SERVER: str = "localhost"
    PORT: int | None = None
    USER: str | None = None
    PASSWORD: str | None = None
    NAME: str
    @computed_field
    @property
    def URI(self) -> str:
        uri = self.VENDOR.generate_uri(self.NAME)
        return uri