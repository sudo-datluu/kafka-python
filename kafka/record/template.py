from __future__ import annotations

import abc
import io

from kafka.protocol.decoder import Decoder

class _KafkaRecord(abc.ABC):
    @classmethod
    def decode(cls, byte_stream: io.BufferedIOBase) -> _KafkaRecord:
        pass

def decode_record(byte_stream: io.BufferedIOBase, record_type: type[_KafkaRecord]) -> _KafkaRecord:
    Decoder.decode_varint(byte_stream)
    Decoder.decode_int8(byte_stream)
    Decoder.decode_varlong(byte_stream)
    Decoder.decode_varint(byte_stream)
    Decoder.decode_compact_bytes(byte_stream)
    Decoder.decode_varint(byte_stream)
    Decoder.decode_int8(byte_stream)
    record_type = Decoder.decode_int8(byte_stream)
    Decoder.decode_int8(byte_stream)

    match record_type:
        case 2:
            from kafka.record.topic import Topic
            record_class = Topic
        case 3:
            from kafka.record.partition import Partition
            record_class = Partition
        case 12:
            from kafka.record.feature_level import FeatureLevel
            record_class = FeatureLevel
        case _:
            raise ValueError(f"Unknown record type: {record_type}")
        
    record = record_class.decode(byte_stream)
    assert byte_stream.read(1) == b"\x00", "Unexpected tagged fields."
    return record