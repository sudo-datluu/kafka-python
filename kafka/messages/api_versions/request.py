from __future__ import annotations
from kafka.messages.request import _KafkaRequestBody
from kafka.protocol.decoder import Decoder

import dataclasses
import io

@dataclasses.dataclass
class ApiVersionsRequestBody(_KafkaRequestBody):
    client_software_name: str
    client_software_version: str

    @classmethod
    def decode(cls, byte_stream: io.BufferedIOBase) -> ApiVersionsRequestBody:
        request_body = ApiVersionsRequestBody(
            client_software_name=Decoder.decode_compact_string(byte_stream),
            client_software_version=Decoder.decode_compact_string(byte_stream)
        )
        Decoder.decode_tagged_fields(byte_stream)
        return request_body