from __future__ import annotations

import dataclasses
import abc

from kafka.protocol import ApiKey, Decoder, Encoder
from .request import _KafkaRequestHeader, KafkaRequest

@dataclasses.dataclass
class _KafkaResponseHeader:
    api_key: ApiKey # Define the header format
    correlation_id: int

    @classmethod
    def from_request_header(cls, request_header: _KafkaRequestHeader) -> _KafkaResponseHeader:
        return _KafkaResponseHeader(
            api_key=request_header.api_key,
            correlation_id=request_header.correlation_id
        )

    def encode(self) -> bytes:
        if self.api_key == ApiKey.API_VERSIONS:
            return Encoder.encode_int32(self.correlation_id)
        return Encoder.encode_int32(self.correlation_id) + Encoder.encode_tagged_fields()
    
    def __str__(self) -> str:
        return f"[KAFKA RESPONSE HEADER] API Key: {self.api_key}, Correlation ID: {self.correlation_id}"
    
class _KafkaResponseBody(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def from_request(cls, request: KafkaRequest) -> _KafkaResponseBody:
        raise NotImplementedError

    @abc.abstractmethod
    def encode(self) -> bytes:
        raise NotImplementedError
    
@dataclasses.dataclass
class KafkaResponse:
    header: _KafkaResponseHeader
    body: _KafkaResponseBody

    @classmethod
    def from_request(cls, request: KafkaRequest) -> KafkaResponse:
        header = _KafkaResponseHeader.from_request_header(request.header)

        match request.header.api_key:
            case ApiKey.API_VERSIONS:
                from .api_versions.response import ApiVersionsResponseBody
                body_class = ApiVersionsResponseBody
        return KafkaResponse(header, body_class.from_request(request))

    def encode(self) -> bytes:
        message = self.header.encode() + self.body.encode()
        return Encoder.encode_int32(len(message)) + message
    
    def __str__(self) -> str:
        outstream = "\n"
        outstream += f"{self.header}"
        outstream += f"{self.body}\n"
        return f"[KAFKA RESPONSE]{outstream}"