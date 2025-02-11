from pydantic_settings import BaseSettings, SettingsConfigDict


class Metadata(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      env_prefix='METADATA_',
                                      env_ignore_empty=True,
                                      extra="ignore")
    NAME: str = "WeCluck"
    DESCRIPTION: str = "Chicken-based per-topic forum."
    AUTHOR: str = "Hanoch Y"
    VERSION: str = "1.0.0"