from functools import lru_cache
from config.apps._schema import AppSettings
from config.dbs._schema import DBSettings

from config.apps.main import MainApp
from config.dbs.forum import ForumDB
from config.loggers.main import LOGGING_CONFIG
from config.metadata import Metadata


class ConfigProvider():
    
    @staticmethod
    @lru_cache(maxsize=1)
    def main_app_settings(production: bool = False) -> AppSettings:
        if production: return MainApp.Production()
        else: return MainApp.Development()

    @staticmethod
    @lru_cache(maxsize=1)
    def forum_db_settings(production: bool = False) -> DBSettings:
        if production: return ForumDB.Production() 
        else: return ForumDB.Development()
    
    @staticmethod
    @lru_cache(maxsize=1)
    def metadata() -> Metadata:
        return Metadata()
    
    @staticmethod
    @lru_cache(maxsize=1)
    def logging_settings():
        return LOGGING_CONFIG
