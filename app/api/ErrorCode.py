from enum import unique, Enum

@unique
class ErrorCode(Enum):
    NO_ERROR = 0
    UNSUPPORTED_VERSION = 35