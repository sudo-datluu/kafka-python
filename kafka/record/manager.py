from __future__ import annotations
import io
import uuid
from typing import Generator, Optional

from kafka.record.partition import Partition
from kafka.record.topic import Topic

from kafka.record.batch import BatchRecord

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class RecordManager(metaclass=SingletonMeta):
    def __init__(self, cluster_meta_data_path='/tmp/kraft-combined-logs/__cluster_metadata-0/00000000000000000000.log'):
        self._topics: list[Topic] = []
        self._partitions: list[Partition] = []

        with io.open(cluster_meta_data_path, 'rb') as byte_stream:
            while byte_stream.peek():
                batch_record = BatchRecord.decode(byte_stream)

                for record in batch_record.records:
                    if type(record) == Topic:
                        self._topics.append(record)
                    elif type(record) == Partition:
                        self._partitions.append(record)
    
    def get_topic(self, topic_name: str) -> Optional[Topic]:
        for topic in self._topics:
            if topic.name == topic_name:
                return topic
    
    def get_partitions(self, topic_id: uuid.UUID) -> Generator[Partition, None, None]:
        for partition in self._partitions:
            if partition.topic_id == topic_id:
                yield partition