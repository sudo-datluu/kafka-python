from __future__ import annotations
import dataclasses
import io

from kafka.protocol.decoder import Decoder
from kafka.record.template import _KafkaRecord

@dataclasses.dataclass
class FeatureLevel(_KafkaRecord):
    name: str
    feature_level: int

    @classmethod
    def decode(cls, byte_stream: io.BufferedIOBase) -> FeatureLevel:
        record = FeatureLevel(
            name=Decoder.decode_compact_string(byte_stream),
            feature_level=Decoder.decode_int16(byte_stream)
        )
        Decoder.decode_tagged_fields(byte_stream)
        return record