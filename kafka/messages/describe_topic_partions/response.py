from __future__ import annotations

import dataclasses
import uuid

# from kafka.messages.describe_topic_partions.cursor import Cursor
from kafka.messages.request import KafkaRequest
from kafka.protocol import Decoder, ErrorCode, Encoder
from kafka.messages.response import _KafkaResponseBody
from kafka.messages.describe_topic_partions.topic import TopicItemResponse
from kafka.messages.describe_topic_partions.request import DescribeTopicPartionsRequestBody
from kafka.record.manager import RecordManager


@dataclasses.dataclass
class DescribeTopicPartionsResponseBody(_KafkaResponseBody):
    throttle_time_ms: int
    topics: list[TopicItemResponse]
    # next_cursor: Cursor

    @classmethod
    def from_request(cls, request: KafkaRequest) -> DescribeTopicPartionsResponseBody:
        assert type(request.body) is DescribeTopicPartionsRequestBody, f"Expected {DescribeTopicPartionsRequestBody}, got {type(request.body)}"

        record_manger = RecordManager()

        return DescribeTopicPartionsResponseBody(
            throttle_time_ms=0,
            topics=[TopicItemResponse.from_topic_name(topic.name, record_manger) for topic in request.body.topics],
            # next_cursor=request.body.cursor
        )
    
    def encode(self) -> bytes:
        return b"".join([
            Encoder.encode_int32(self.throttle_time_ms),
            Encoder.encode_compact_array(self.topics),
            b"\xff",
            Encoder.encode_tagged_fields()
        ])
