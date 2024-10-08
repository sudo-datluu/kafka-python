from __future__ import annotations

import dataclasses
import io

from kafka.protocol.decoder import Decoder
from kafka.messages.request import _KafkaRequestBody
# from kafka.messages.describe_topic_partions.cursor import Cursor
from kafka.messages.describe_topic_partions.topic import TopicItemRequest

@dataclasses.dataclass
class DescribeTopicPartionsRequestBody(_KafkaRequestBody):
    topics: list[TopicItemRequest]
    response_partition_limit: int

    @classmethod
    def decode(cls, byte_stream: io.BytesIO) -> DescribeTopicPartionsRequestBody:
        request_body = DescribeTopicPartionsRequestBody(
            topics=Decoder.decode_compact_array(byte_stream=byte_stream, decoder=TopicItemRequest.decode),
            response_partition_limit=Decoder.decode_int32(byte_stream),
        )
        cursor = byte_stream.read(1)
        assert cursor == b"\xff", f"Only null cursor is supported, Got {cursor}"
        Decoder.decode_tagged_fields(byte_stream)
        return request_body