
import json
from typing import Annotated

from pydantic import AnyUrl, field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from utils.enums.environments import Environment

class AppSettings(BaseSettings):
    pass
