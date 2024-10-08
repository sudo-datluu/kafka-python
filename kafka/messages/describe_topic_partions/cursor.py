from __future__ import annotations

import dataclasses
import io

@dataclasses.dataclass
class Cursor:
    @classmethod
    def decode(cls, byte_stream: io.BufferedIOBase) -> Cursor:
        assert byte_stream.read(1) == b"\xff", "Cursor should be null"
        # byte_stream.read(1)
        cursor = Cursor()
        return cursor

    def encode(self) -> bytes:
        return b"\xff"