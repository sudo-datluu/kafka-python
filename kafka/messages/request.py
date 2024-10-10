from __future__ import annotations
from kafka.protocol.api_key import ApiKey
from kafka.protocol.decoder import Decoder
from kafka.protocol.encoder import Encoder

import dataclasses
import io
import asyncio
import abc

# Define a dataclass for the request header
@dataclasses.dataclass
class _KafkaRequestHeader:
    api_key: ApiKey
    api_version: int
    correlation_id: int
    client_id: str

    @classmethod
    def decode(cls, byte_stream: io.BufferedIOBase) -> _KafkaRequestHeader:
        api_key = ApiKey.decode(byte_stream)
        print(api_key)
        api_version = Decoder.decode_int16(byte_stream)
        print(api_version)
        correlation_id = Decoder.decode_int32(byte_stream)
        print(correlation_id)
        client_id = Decoder.decode_nullable_string(byte_stream)
        print(client_id)
        Decoder.decode_tagged_fields(byte_stream)
        return _KafkaRequestHeader(api_key, api_version, correlation_id, client_id)

    def __str__(self) -> str:
        return f"[KAFKA REQUEST HEADER] API Key: {self.api_key}, API Version: {self.api_version}, Correlation ID: {self.correlation_id}, Client ID: {self.client_id}"

# Define an abstract class for the request body
class _KafkaRequestBody(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def decode(cls, byte_stream: io.BufferedIOBase) -> _KafkaRequestBody:
        raise NotImplementedError

@dataclasses.dataclass
class KafkaRequest:
    header: _KafkaRequestHeader
    body: _KafkaRequestBody

    # Return a KafkaRequest object from a stream reader
    @classmethod
    async def from_stream_reader(cls, stream_reader: asyncio.StreamReader) -> KafkaRequest:
        message_length = int.from_bytes(await stream_reader.readexactly(4), byteorder='big')
        byte_stream = io.BytesIO(await stream_reader.readexactly(message_length))

        print(f"Raw data: {Encoder.encode_int32(message_length) + byte_stream.getvalue()}")
        request_header = _KafkaRequestHeader.decode(byte_stream)
        match request_header.api_key:
            # Handle the case where the API key is API_VERSIONS
            case ApiKey.API_VERSIONS:
                from kafka.messages.api_versions.request import ApiVersionsRequestBody
                request_body_class = ApiVersionsRequestBody
            # Handle the case where the API key is DESCRIBE_TOPIC_PARTITIONS
            case ApiKey.DESCRIBE_TOPIC_PARTITIONS:
                from kafka.messages.describe_topic_partions.request import DescribeTopicPartionsRequestBody
                request_body_class = DescribeTopicPartionsRequestBody
        return KafkaRequest(request_header, request_body_class.decode(byte_stream))

    def __str__(self) -> str:
        return f"{self.header}\n{self.body}"
                