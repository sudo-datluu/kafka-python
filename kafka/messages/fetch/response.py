from __future__ import annotations
import dataclasses
import io
import uuid

from kafka.protocol.encoder import Encoder
from kafka.protocol.errors_code import ErrorCode
from kafka.messages.request import KafkaRequest
from kafka.messages.response import _KafkaResponseBody
from kafka.messages.fetch.request import FetchRequestBody

@dataclasses.dataclass
class FetchReponseBody(_KafkaResponseBody):
    throttle_time_ms: int
    error_code: ErrorCode
    session_id: int
    responses: list[_FetchResponseItem]

    @classmethod
    def from_request(cls, request: KafkaRequest) -> FetchReponseBody:
        assert type(request.body) is FetchRequestBody, f"Expected FetchRequestBody but got {type(request.body)}"
        if not request.body.topics:
            return FetchReponseBody(
                throttle_time_ms=0,
                error_code=ErrorCode.NO_ERROR,
                session_id=request.body.session_id,
                responses=[]
            )
        topic_items = request.body.topics[0]
        response_items = _FetchResponseItem(
            topic_id=topic_items.topic_id,
            partitions=[ _FetchResponsePartition(partition_index=0, error_code=ErrorCode.UNKNOWN_TOPIC_ID) ]
        )
        return FetchReponseBody(
            throttle_time_ms=0,
            error_code=ErrorCode.NO_ERROR,
            session_id=request.body.session_id,
            responses=[response_items]
        )

    def encode(self) -> bytes:
        return b"".join([
            Encoder.encode_int32(self.throttle_time_ms),
            self.error_code.encode(),
            Encoder.encode_int32(self.session_id),
            Encoder.encode_compact_array(self.responses, _FetchResponseItem.encode),
            Encoder.encode_tagged_fields(),
        ])

@dataclasses.dataclass
class _FetchResponseItem:
    topic_id: uuid.UUID
    partitions: list[_FetchResponsePartition]
    def encode(self) -> bytes:
        return b"".join([
            Encoder.encode_uuid(self.topic_id),
            Encoder.encode_compact_array(self.partitions, _FetchResponsePartition.encode),
            Encoder.encode_tagged_fields(),
        ])

@dataclasses.dataclass
class _FetchResponsePartition:
    partition_index: int
    error_code: ErrorCode
    high_watermark: int = 0
    last_stable_offset: int = 0
    log_start_offset: int = 0
    aborted_transactions: list[_FetchAbortedTransaction] = dataclasses.field(default_factory=list)
    preferred_read_replica: int = 0

    def encode(self) -> bytes:
        return b"".join([
            Encoder.encode_int32(self.partition_index),
            self.error_code.encode(),
            Encoder.encode_int64(self.high_watermark),
            Encoder.encode_int64(self.last_stable_offset),
            Encoder.encode_int64(self.log_start_offset),
            Encoder.encode_compact_array(self.aborted_transactions),
            Encoder.encode_int32(self.preferred_read_replica),
            Encoder.encode_compact_array([]),
            Encoder.encode_tagged_fields(),
        ])

@dataclasses.dataclass
class _FetchAbortedTransaction:
    producer_id: int
    first_offset: int

    @classmethod
    def encode(self) -> bytes:
        return b"".join([
            Encoder.encode_int64(self.producer_id),
            Encoder.encode_int64(self.first_offset),
            Encoder.encode_tagged_fields(),
        ])