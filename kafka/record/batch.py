from __future__ import annotations
import dataclasses
import io

from kafka.protocol.decoder import Decoder

from kafka.record.template import _KafkaRecord, decode_record

@dataclasses.dataclass
class BatchRecord:
    base_offset: int
    batch_length: int
    partition_leader_epoch: int
    magic: int
    crc: int
    attributes: int
    last_offset_delta: int
    base_timestamp: int
    max_timestamp: int
    producer_id: int
    producer_epoch: int
    base_sequence: int
    records: list[_KafkaRecord]

    @classmethod
    def decode(cls, byte_stream: io.BufferedIOBase) -> BatchRecord:
        base_offset = Decoder.decode_int64(byte_stream)
        batch_length = Decoder.decode_int32(byte_stream)
        partition_leader_epoch = Decoder.decode_int32(byte_stream)
        magic = Decoder.decode_int8(byte_stream)
        crc = Decoder.decode_int32(byte_stream)
        attributes = Decoder.decode_int16(byte_stream)
        last_offset_delta = Decoder.decode_int32(byte_stream)
        base_timestamp = Decoder.decode_int64(byte_stream)
        max_timestamp = Decoder.decode_int64(byte_stream)
        producer_id = Decoder.decode_int64(byte_stream)
        producer_epoch = Decoder.decode_int16(byte_stream)
        base_sequence = Decoder.decode_int32(byte_stream)
        record_count = Decoder.decode_int32(byte_stream)
        records = [decode_record(byte_stream, _KafkaRecord) for _ in range(record_count)]


        return BatchRecord(
            base_offset=base_offset,
            batch_length=batch_length,
            partition_leader_epoch=partition_leader_epoch,
            magic=magic,
            crc=crc,
            attributes=attributes,
            last_offset_delta=last_offset_delta,
            base_timestamp=base_timestamp,
            max_timestamp=max_timestamp,
            producer_id=producer_id,
            producer_epoch=producer_epoch,
            base_sequence=base_sequence,
            records=records
        )