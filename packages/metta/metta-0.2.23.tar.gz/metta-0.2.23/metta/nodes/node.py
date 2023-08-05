import asyncio
import random
import logging
import uvloop

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer, ConsumerRecord, TopicPartition
from typing import (
    Awaitable,
    AsyncGenerator,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    NamedTuple,
    Union,
)
from nptyping import NDArray
from contextlib import AsyncExitStack
from queue import Queue
from functools import partial
from multiprocessing import Process

from metta.common import profiler, shared_memory, time_utils
from metta.common.shared_memory import SharedMemoryClient
from metta.common.topics import ProtobufMessage, Topic, Message, MessageData, NewMessage
from metta.common.topic_registry import TopicRegistry
from metta.proto.trace_pb2 import Trace
from metta.proto.topic_pb2 import DataLocation, TopicMessage


class Node(AsyncExitStack):
    def __init__(
        self,
        *,
        kafka_brokers: List[str],
        zookeeper_hosts: List[str],
        source_topic: Optional[Topic] = None,
        publish_topic: Optional[Topic] = None,
        event_loop: Optional[asyncio.unix_events._UnixSelectorEventLoop] = None,
    ):
        self.source_topic = source_topic
        self.publish_topic = publish_topic

        self.kafka_brokers = kafka_brokers
        self.zk_hosts = zookeeper_hosts
        self.event_loop = event_loop

        self.consumer = None
        self.producer = None

    def _make_client_id(self) -> str:
        return f"{self.source_topic}->{self.publish_topic}-{random.randint(0,100)}"

    async def _init_kafka_connections(self) -> None:
        client_id = self._make_client_id()
        if self.source_topic:
            self.consumer = AIOKafkaConsumer(
                self.source_topic,
                loop=self.event_loop,
                bootstrap_servers=self.kafka_brokers,
                client_id=client_id,
            )
            await self.consumer.start()
            logging.debug(f"Initialized consumer for topic {self.source_topic}")
        if self.publish_topic:
            self.producer = AIOKafkaProducer(
                loop=self.event_loop,
                bootstrap_servers=self.kafka_brokers,
                client_id=client_id,
            )
            await self.producer.start()
            logging.debug(f"Initialized producer for topic {self.publish_topic}")

    async def _init_topic_registry(self):
        self.topic_registry = TopicRegistry(
            kafka_brokers=self.kafka_brokers, zookeeper_hosts=self.zk_hosts
        )
        async with self.topic_registry as registry:
            await registry.sync()

    async def __aenter__(self):
        if self.event_loop is None:
            self.event_loop = asyncio.get_event_loop()
        self.shm_client = SharedMemoryClient()
        await self._init_topic_registry()
        await self._init_kafka_connections()
        return self

    async def __aexit__(self, __exc_type, __exc_value, __traceback):
        if self.consumer:
            await self.consumer.stop()
        if self.producer:
            await self.producer.stop()

    async def _publish(self, msg: NewMessage, trace: Optional[Trace] = None):
        topic_msg = TopicMessage(
            topic_name=self.publish_topic.name,
            source=msg.source,
            timestamp=msg.timestamp,
        )
        if self.publish_topic.data_location == DataLocation.MESSAGE:
            topic_msg.data = msg.data.SerializeToString()
        elif self.publish_topic.data_location == DataLocation.CPU_NDARRAY:
            plasma_obj_id = self.shm_client.write(msg.data, compress=True)
            topic_msg.data = shared_memory.object_id_to_bytes(plasma_obj_id)
        else:
            raise NotImplementedError

        await self.producer.send(
            self.publish_topic.name,
            value=topic_msg.SerializeToString(),
            key=msg.source,
            timestamp_ms=msg.timestamp,
        )

    async def _parse(self, msg: str) -> Message:
        topic_msg = TopicMessage.FromString(msg)
        topic = self.topic_registry[topic_msg.type_name]

        data = None
        if topic.data_location == DataLocation.MESSAGE:
            data = topic.type.FromString(topic.data)
        elif topic.data_location == DataLocation.CPU_NDARRAY:
            plasma_object_id = shared_memory.object_id_from_bytes(topic_msg.data)
            data = self.shm_client.read(plasma_object_id)
        else:
            raise NotImplementedError

        return Message(topic=topic, msg=topic_msg, data=data)

    async def process(
        self,
        input_msg: Message,
    ) -> Optional[NewMessage]:
        raise NotImplementedError

    async def _process(
        self,
        input_msg: Message,
        profile: bool = False,
    ) -> Optional[NewMessage]:
        output_msg = await self.process(input_msg)
        if output_msg is not None and profile:
            trace = input_msg.msg.trace
            if trace is None:
                trace = profiler.init_trace()
            profiler.touch_trace(trace, self.publish_topic)
            output_msg.trace = trace
        return output_msg

    async def run(
        self,
        start_ts: Optional[int] = None,
        end_ts: Optional[int] = None,
        profile: bool = False,
    ) -> None:
        if start_ts is not None:
            pass

        async for record in self.consumer():
            input_msg = await self._parse(record.value)
            output_msg = await self._process(input_msg)
            if output_msg is not None:
                await self._publish(output_msg)
            if end_ts is not None and input_msg.timestamp >= end_ts:
                break

    def register(self, forward_fn: Callable[[List[Message]], Optional[NewMessage]]):
        def _fn(self, fn, inputs):
            return fn(inputs)

        self.process = partial(_fn, self, forward_fn)

    def mainloop(
        self,
        start_ts: Optional[int] = None,
        end_ts: Optional[int] = None,
        profile: Optional[bool] = False,
    ) -> Process:
        def _run():
            async def exec():
                async with self as node:
                    await node.run(start_ts, end_ts, profile)

            uvloop.install()
            asyncio.run(exec())

        p = Process(target=_run)
        p.start()
        return p
