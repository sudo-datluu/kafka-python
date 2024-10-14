from __future__ import annotations

import dataclasses
import io
import uuid

from kafka.protocol.decoder import Decoder
from kafka.messages.describe_topic_partitions.record.template import _KafkaRecord

@dataclasses.dataclass
class Partition(_KafkaRecord):
    partition_id: int
    topic_id: uuid.UUID
    replicas: list[int]
    in_sync_replicas: list[int]
    removing_replicas: list[int]
    adding_replicas: list[int]
    leader: int
    leader_epoch: int
    partition_epoch: int
    directories: list[uuid.UUID]

    @classmethod
    def decode(cls, byte_stream: io.BufferedIOBase) -> Partition:
        record = Partition(
            partition_id=Decoder.decode_int32(byte_stream),
            topic_id=Decoder.decode_uuid(byte_stream),
            replicas=Decoder.decode_compact_array(byte_stream, Decoder.decode_int32),
            in_sync_replicas=Decoder.decode_compact_array(byte_stream, Decoder.decode_int32),
            removing_replicas=Decoder.decode_compact_array(byte_stream, Decoder.decode_int32),
            adding_replicas=Decoder.decode_compact_array(byte_stream, Decoder.decode_int32),
            leader=Decoder.decode_int32(byte_stream),
            leader_epoch=Decoder.decode_int32(byte_stream),
            partition_epoch=Decoder.decode_int32(byte_stream),
            directories=Decoder.decode_compact_array(byte_stream, Decoder.decode_uuid)
        )
        Decoder.decode_tagged_fields(byte_stream)
        return record