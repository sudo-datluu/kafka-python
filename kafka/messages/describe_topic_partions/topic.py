from __future__ import annotations
from kafka.protocol import Decoder, Encoder, ErrorCode
from kafka.record.manager import RecordManager

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

    @classmethod
    def from_topic_name(cls, topic_name: str, record_manager: RecordManager) -> TopicItemResponse:
        topic_record = record_manager.get_topic(topic_name)

        if topic_record is None:
            return TopicItemResponse(
                error_code=ErrorCode.UNKNOWN_TOPIC_OR_PARTITION,
                name=topic_name,
                topic_id=uuid.UUID(int=0),
                is_internal=False,
                partitions=[],
                topic_authorized_operations=0
            )

        topic_id = topic_record.topic_id
        partitions = [
            _PartitionItem(error_code=ErrorCode.NO_ERROR, partition_index=partition_record.partition_id)
            for partition_record in record_manager.get_partitions(topic_id)
        ]
        partitions.sort(key=lambda p: p.partition_index)

        return TopicItemResponse(
            error_code=ErrorCode.NO_ERROR,
            name=topic_name,
            topic_id=topic_id,
            is_internal=False,
            partitions=partitions,
            topic_authorized_operations=0
        )

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
    error_code: ErrorCode
    partition_index: int
    leader_id: int = 0
    leader_epoch: int = 0
    replica_nodes: list[int] = dataclasses.field(default_factory=list)
    isr_nodes: list[int] = dataclasses.field(default_factory=list)
    eligible_leader_replicas: list[int] = dataclasses.field(default_factory=list)
    last_know_elr: list[int] = dataclasses.field(default_factory=list)
    offline_replicas: list[int] = dataclasses.field(default_factory=list)

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