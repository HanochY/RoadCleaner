from typing import Annotated
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from utils.db_vendors import Vendor
from utils.enums.environments import Environment
from pydantic import computed_field

class DBSettings(BaseSettings):
    pass