import asyncio
import random
import logging
import uvloop

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer, ConsumerRecord, TopicPartition
from typing import (
    Awaitable,
    AsyncGenerator,
    Callable,
    Deque,
    Dict,
    List,
    Iterable,
    Optional,
    Tuple,
    Type,
)
from contextlib import AsyncExitStack
from functools import partial
from multiprocessing import Process
from collections import deque, defaultdict

from metta.common import profiler, shared_memory, time_utils
from metta.common.shared_memory import SharedMemoryClient
from metta.common.topics import ProtobufMessage, TopicRegistry, Topic
from metta.proto.trace_pb2 import Trace
from metta.proto.topic_pb2 import DataLocation, TopicMessage
from metta.nodes.node import Node, Message, NewMessage


class SourceSyncNode(Node):
    def __init__(
        self,
        *,
        kafka_brokers: List[str],
        zookeeper_hosts: List[str],
        source_topic: Topic,
        publish_topic: Topic,
        sync_source_sets: Iterable[Tuple[str, ...]],
        max_buffer_size: int = 10,
        event_loop: Optional[asyncio.unix_events._UnixSelectorEventLoop] = None,
    ):
        super().__init__(
            source_topics=[source_topic],
            publish_topic=publish_topic,
            kafka_brokers=kafka_brokers,
            zookeeper_hosts=zookeeper_hosts,
            event_loop=event_loop,
        )

        self.sync_source_sets = sync_source_sets
        self.queues: Dict[Tuple[str, ...], [Dict[str, Deque[Message]]]] = {
            source_set: {
                {source: deque(maxlen=max_buffer_size) for source in source_set}
            }
            for source_set in self.sync_source_sets
        }

        if publish_topic.data_location is DataLocation.CPU_NDArray:
            raise Exception(
                "Invalid data location for synchronized publish topic. Cannot ensure data locality."
            )

    async def _init_kafka_connections(self) -> None:
        client_id = self._make_client_id()

        if self.source_topics:
            self.consumer = AIOKafkaConsumer(
                *self.source_topic,
                loop=self.event_loop,
                bootstrap_servers=self.kafka_brokers,
                client_id=client_id,
                group_id=self.group_id,
            )
            await self.consumer.start()
            logging.debug(f"Initialized consumer for topics {self.source_topics}")

        if self.publish_topic:
            self.producer = AIOKafkaProducer(
                loop=self.event_loop,
                bootstrap_servers=self.kafka_brokers,
                client_id=client_id,
            )
            await self.producer.start()
            logging.debug(f"Initialized producer")

    async def __aenter__(self):
        if self.event_loop is None:
            self.event_loop = asyncio.get_event_loop()

        await self._init_topic_registry()
        await self._make_plasma_connection()
        await self._init_kafka_connections()
        return self

    async def sync(
        self,
        sources: List[Deque[Message]],
    ) -> NewMessage:
        pass

    async def process(
        self,
        input_msg: Message,
    ) -> List[NewMessage]:
        topic, topic_msg, data = input_msg
        new_synced = []
        for source_set in self.sync_source_sets:
            source_set_queues = self.queues[source_set]
            if topic_msg.source in source_set:
                source_set_queues[topic_msg.source].append(input_msg)
                synced = await self.sync(source_set_queues)
                if synced is not None:
                    new_synced.append(
                        NewMessage(
                            source="-".join(source_set),
                            timestamp=input_msg.timestamp,
                            data=synced,
                        )
                    )
        return new_synced

    async def run(
        self,
        start_ts: Optional[int] = None,
        end_ts: Optional[int] = None,
        profile: Optional[bool] = False,
    ) -> None:
        if start_ts is not None:
            raise NotImplementedError

        async for record in self.consumer:
            input_msg = await self._parse(record.value)
            output_msg = await self.process(input_msg)
            if output_msg is not None:
                await self._publish(output_msg)
            if end_ts is not None and input_msg.timestamp >= end_ts:
                break
