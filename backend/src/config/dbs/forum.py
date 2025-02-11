

from config.dbs._schema import DBSettings
from utils.db_vendors import Vendor, VENDOR_SQLITE
from pydantic_settings import SettingsConfigDict
from utils.enums.environments import Environment

class ForumDB:
    class Development(DBSettings):
        model_config = SettingsConfigDict(env_file='.env',
                                          env_prefix='FORUM_DB_',
                                          env_ignore_empty=True,
                                          extra="ignore")
        NAME: str = r"development-forum.sqlite3"
        VENDOR: Vendor = VENDOR_SQLITE
        ENVIRONMENT: Environment = Environment.DEVELOPMENT
#        @computed_field
#        @property
#        def URI(self) -> str:
#            uri = self.VENDOR.generate_uri(self.NAME)
#            return uri

    class Production(DBSettings):
        model_config = SettingsConfigDict(env_file='.env',
                                          env_prefix='FORUM_DB_',
                                          env_ignore_empty=True,
                                          extra="ignore")
        NAME: str = r"forum.sqlite3"
        VENDOR: Vendor = VENDOR_SQLITE
        ENVIRONMENT: Environment = Environment.PRODUCTION
#        @computed_field
#        @property
#        def URI(self) -> str:
#            uri = self.VENDOR.generate_uri(self.NAME)
#            return uri
