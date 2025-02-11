from enum import auto
from typing import Callable, Any
class Vendor:
    name: str
    generate_uri: Callable[[Any], str]
    def __init__(self, name: str, generate_uri: Callable[[Any], str]):
        self.name = name
        self.generate_uri = generate_uri
    
def generate_sqlite_uri(name):
    return f"sqlite:///{name}"

def generate_mongodb_uri(user: str, password: str, server: str, port: int, name: str):
    return f"mongodb://{user}:{password}@{server}:{port}/{name}"

VENDOR_SQLITE = Vendor(
    name = auto(),
    generate_uri = generate_sqlite_uri
)
VENDOR_MONGODB = Vendor(
    name = auto(),
    generate_uri = generate_mongodb_uri
)