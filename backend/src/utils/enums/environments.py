from enum import auto
from strenum import UppercaseStrEnum

class Environment(UppercaseStrEnum):
    DEVELOPMENT = auto()
    PRODUCTION = auto()
