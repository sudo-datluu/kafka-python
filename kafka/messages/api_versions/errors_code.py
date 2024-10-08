from __future__ import annotations
from ...protocol.decoder import Decoder
from ...protocol.encoder import Encoder

import io
import enum

@enum.unique
class ErrorCode(enum.IntEnum):
    NO_ERROR = 0
    UNSUPPORTED_VERSION = 35

    @classmethod
    def decode(cls, byte_stream: io.BytesIO) -> ErrorCode:
        return ErrorCode(Decoder.decode_int16(byte_stream))
    
    def encode(self) -> bytes:
        return Encoder.encode_int16(self.value)