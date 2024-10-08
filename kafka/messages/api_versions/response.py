from __future__ import annotations
import dataclasses

from kafka.messages.request import KafkaRequest

from .errors_code import ErrorCode
from .request import ApiVersionsRequestBody
from kafka.messages.response import _KafkaResponseBody
from kafka.protocol import ApiKey, Encoder

SUPPORTED_API_VERSIONS = [0, 1, 2, 3, 4]

@dataclasses.dataclass
class ApiKeyItem:
    api_key: ApiKey
    min_version: int
    max_version: int

    def encode(self) -> bytes:
        return b"".join([
            self.api_key.encode(),
            Encoder.encode_int16(self.min_version),
            Encoder.encode_int16(self.max_version),
            Encoder.encode_tagged_fields()
        ])

    def __str__(self) -> str:
        return f"<Key: {self.api_key}, Min version: {self.min_version}, Max version: {self.max_version}>"

@dataclasses.dataclass
class ApiVersionsResponseBody(_KafkaResponseBody):
    error_code: ErrorCode
    api_keys: list[ApiKeyItem]
    throttle_time_ms: int

    @classmethod
    def from_request(cls, request: KafkaRequest) -> _KafkaResponseBody:
        assert type(request.body) is ApiVersionsRequestBody, f"Expected {ApiVersionsRequestBody}, got {type(request.body)}"

        error_code = ErrorCode.NO_ERROR if request.header.api_version in SUPPORTED_API_VERSIONS else ErrorCode.UNSUPPORTED_VERSION

        return ApiVersionsResponseBody(
            error_code = error_code,
            api_keys = [
                ApiKeyItem(ApiKey.API_VERSIONS, min_version=0, max_version=4),
                ApiKeyItem(ApiKey.DESCRIBE_TOPIC_PARTITIONS, min_version=0, max_version=0),
            ],
            throttle_time_ms=0
        )

    def encode(self) -> bytes:
        return b"".join([
            self.error_code.encode(),
            Encoder.encode_compact_array(self.api_keys, ApiKeyItem.encode),
            Encoder.encode_int32(self.throttle_time_ms),
            Encoder.encode_tagged_fields()
        ])

    def __str__(self) -> str:
        outstream = "\n"
        outstream += f"[KAFKA REPONSE BODY]\n"
        outstream += f"- Error: {self.error_code}\n"
        outstream += f"- API Keys:\n"
        for api_key in self.api_keys:
            outstream += f"  + {api_key}\n"
        outstream += f"- Throttle Time: {self.throttle_time_ms}"
        return f"{outstream}"