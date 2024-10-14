from __future__ import annotations

import dataclasses
import io
import uuid

from kafka.protocol.decoder import Decoder
from kafka.record.template import _KafkaRecord

@dataclasses.dataclass
class Topic(_KafkaRecord):
    name: str
    topic_id: uuid.UUID

    @classmethod
    def decode(cls, byte_stream: io.BufferedIOBase) -> _KafkaRecord:
        record = Topic(
            name=Decoder.decode_compact_string(byte_stream),
            topic_id=Decoder.decode_uuid(byte_stream)
        )
        Decoder.decode_tagged_fields(byte_stream)
        return record