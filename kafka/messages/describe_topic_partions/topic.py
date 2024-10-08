from __future__ import annotations
from kafka.protocol import Decoder, Encoder, ErrorCode
import io
import dataclasses
import uuid

@dataclasses.dataclass
class TopicItemRequest:
    name: str

    @classmethod
    def decode(cls, byte_stream: io.BytesIO) -> TopicItemRequest:
        item = TopicItemRequest(
            name=Decoder.decode_compact_string(byte_stream)
        )
        Decoder.decode_tagged_fields(byte_stream)
        return item
    
@dataclasses.dataclass
class TopicItemResponse:
    error_code: ErrorCode
    name: str
    topic_id: uuid.UUID
    is_internal: bool
    partitions: list[_PartitionItem]
    topic_authorized_operations: int

    def encode(self) -> bytes:
        return b"".join([
            self.error_code.encode(),
            Encoder.encode_compact_nullable_string(self.name),
            Encoder.encode_uuid(self.topic_id),
            Encoder.encode_boolean(self.is_internal),
            Encoder.encode_compact_array(self.partitions, _PartitionItem.encode),
            Encoder.encode_int32(self.topic_authorized_operations),
            Encoder.encode_tagged_fields(),
        ])
    
@dataclasses.dataclass
class _PartitionItem:
    name: str
    error_code: ErrorCode
    partition_index: int
    leader_id: int
    leader_epoch: int
    replica_nodes: list[int]
    isr_nodes: list[int]
    eligible_leader_replicas: list[int]
    last_know_elr: list[int]
    offline_replicas: list[int]

    def encode(self) -> bytes:
        return b"".join([
            self.error_code.encode(),
            Encoder.encode_int32(self.partition_index),
            Encoder.encode_int32(self.leader_id),
            Encoder.encode_int32(self.leader_epoch),
            Encoder.encode_compact_array(self.replica_nodes, Encoder.encode_int32),
            Encoder.encode_compact_array(self.isr_nodes, Encoder.encode_int32),
            Encoder.encode_compact_array(self.eligible_leader_replicas, Encoder.encode_int32),
            Encoder.encode_compact_array(self.last_know_elr, Encoder.encode_int32),
            Encoder.encode_compact_array(self.offline_replicas, Encoder.encode_int32),
            Encoder.encode_tagged_fields(),
        ])