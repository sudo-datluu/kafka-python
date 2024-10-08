from __future__ import annotations
from .decoder import Decoder
from .encoder import Encoder
import io
import enum

@enum.unique
class ApiKey(enum.IntEnum):
    API_VERSIONS = 18
    DESCRIBE_TOPIC_PARTITIONS = 75

    @classmethod
    def decode(cls, byte_stream: io.BufferedIOBase) -> ApiKey:
        return ApiKey(Decoder.decode_int16(byte_stream))
    
    def encode(self) -> bytes:
        return Encoder.encode_int16(self.value)