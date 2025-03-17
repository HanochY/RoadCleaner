import pickle
from sqlalchemy import Text, TypeDecorator
from cryptography.fernet import Fernet 
from config.provider import ConfigProvider

db_settings = ConfigProvider.forum_db_settings()
default_key = db_settings.KEY

class Encrypted(TypeDecorator):
    impl = Text
    cache_ok = True

    def __init__(self, T: type, encryption_key: str = default_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._type: type = T
        self.encryption_key: str = encryption_key
        self.fernet = Fernet(encryption_key.encode())

    def process_bind_param(self, value):
        if value is not None:
            if isinstance(value, self._type):
                value: str = self.fernet.encrypt(pickle.dumps(value)).decode()
        return value

    def process_result_value(self, value: str):
        if value is not None:
            value = pickle.loads(self.fernet.decrypt(value.encode()))
        if isinstance(value, self._type):
            return value