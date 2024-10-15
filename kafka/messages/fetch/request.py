from __future__ import annotations
import dataclasses
import io
import uuid

from kafka.protocol.decoder import Decoder
from kafka.messages.request import _KafkaRequestBody

@dataclasses.dataclass
class FetchRequestBody(_KafkaRequestBody):
    max_wait_ms: int
    min_bytes: int
    max_bytes: int
    isolation_level: int
    session_id: int
    session_epoch: int
    topics: list[_FetchTopic]
    forgotten_topics: list[_FetchForgottonTopic]
    rack_id: str

    @classmethod
    def decode(cls, byte_stream: io.BufferedIOBase) -> FetchRequestBody:
        request_body = FetchRequestBody(
            max_wait_ms=Decoder.decode_int32(byte_stream),
            min_bytes=Decoder.decode_int32(byte_stream),
            max_bytes=Decoder.decode_int32(byte_stream),
            isolation_level=Decoder.decode_int8(byte_stream),
            session_id=Decoder.decode_int32(byte_stream),
            session_epoch=Decoder.decode_int32(byte_stream),
            topics=Decoder.decode_compact_array(byte_stream, _FetchTopic.decode),
            forgotten_topics=Decoder.decode_compact_array(byte_stream, _FetchForgottonTopic.decode),
            rack_id=Decoder.decode_compact_string(byte_stream)
        )
        Decoder.decode_tagged_fields(byte_stream)
        return request_body

@dataclasses.dataclass
class _FetchTopic:
    topic_id: uuid.UUID
    partitions: list[_FetchPartition]

    @classmethod
    def decode(cls, byte_stream: io.BufferedIOBase) -> _FetchTopic:
        item = _FetchTopic(
            topic_id=Decoder.decode_uuid(byte_stream),
            partitions=Decoder.decode_compact_array(byte_stream, _FetchPartition.decode)
        )
        Decoder.decode_tagged_fields(byte_stream)
        return item


@dataclasses.dataclass
class _FetchPartition:
    partition_id: int
    current_leader_epoch: int
    fetch_offset: int
    last_fetched_epoch: int
    log_start_offset: int
    partition_max_bytes: int

    @classmethod
    def decode(cls, byte_stream: io.BufferedIOBase) -> _FetchPartition:
        item = _FetchPartition(
            partition_id=Decoder.decode_int32(byte_stream),
            current_leader_epoch=Decoder.decode_int32(byte_stream),
            fetch_offset=Decoder.decode_int64(byte_stream),
            last_fetched_epoch=Decoder.decode_int32(byte_stream),
            log_start_offset=Decoder.decode_int64(byte_stream),
            partition_max_bytes=Decoder.decode_int32(byte_stream)
        )
        Decoder.decode_tagged_fields(byte_stream)
        return item

@dataclasses.dataclass
class _FetchForgottonTopic:
    topic_id: uuid.UUID
    partitions: list[int]

    @classmethod
    def decode(cls, byte_stream: io.BufferedIOBase) -> _FetchForgottonTopic:
        item = _FetchForgottonTopic(
            topic_id=Decoder.decode_uuid(byte_stream),
            partitions=Decoder.decode_compact_array(byte_stream, Decoder.decode_int32)
        )
        Decoder.decode_tagged_fields(byte_stream)
        return item