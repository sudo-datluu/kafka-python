from __future__ import annotations
from ..request import _KafkaRequestBody
from ...protocol.decoder import Decoder

import dataclasses
import io

@dataclasses.dataclass
class ApiVersionsRequestBody(_KafkaRequestBody):
    client_software_name: str
    client_software_version: str

    @classmethod
    def decode(cls, byte_stream: io.BufferedIOBase) -> ApiVersionsRequestBody:
        request_body = ApiVersionsRequestBody(
            client_software_name="",
            client_software_version=""
        )
        Decoder.decode_tagged_fields(byte_stream)
        return request_body