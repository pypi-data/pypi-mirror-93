import asyncio
import random
import logging
import uvloop

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer, ConsumerRecord, TopicPartition
from typing import (
    Awaitable,
    AsyncGenerator,
    Callable,
    List,
    Optional,
    Tuple,
    Type,
    NamedTuple,
)
from nptyping import NDArray
from contextlib import AsyncExitStack
from queue import Queue
from functools import partial
from multiprocessing import Process

from metta.common import profiler, shared_memory, time_utils
from metta.common.shared_memory import SharedMemoryClient
from metta.common.topics import ProtobufMessage, TopicRegistry, Topic
from metta.proto.trace_pb2 import Trace
from metta.proto.topic_pb2 import DataLocation, TopicMessage

MessageData = Union[ProtobufMessage, NDArray]


class Message(NamedTuple):
    topic: Topic
    msg: TopicMessage
    data: MessageData


class NewMessage(NamedTuple):
    source: str
    data: MessageData


class Node(AsyncExitStack):
    def __init__(
        self,
        *,
        kafka_brokers: List[str],
        zookeeper_hosts: List[str],
        source_topics: List[Topic],
        publish_topic: Topic,
        synchronize_fn: Callable[List[Message], List[Message]],
        event_loop: Optional[asyncio.unix_events._UnixSelectorEventLoop] = None,
    ):
        self.source_topics = source_topics
        self.publish_topic = publish_topic

        self.group_id = consumer_group_id
        self.kafka_brokers = kafka_brokers
        self.zk_hosts = zookeeper_hosts
        self.event_loop = event_loop

        self.consumer = None
        self.producer = None

    def _make_client_id(self) -> str:
        return f"{'-'.join(self.source_topics)}->{self.publish_topic}-{random.randint(0,100)}"

    async def _init_kafka_connections(self) -> None:
        client_id = self._make_client_id()
        if self.source_topics:
            self.consumer = AIOKafkaConsumer(
                *[topic.name for topic in self.source_topics],
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
            timestamp=time_utils.time_ms(),
        )
        if self.publish_topic.data_location == DataLocation.MESSAGE:
            topic_msg.data = msg.data.SerializeToString()
        elif self.publish_topic.data_location == DataLocation.CPU_NDARRAY:
            plasma_obj_id = self.shm_client.write(msg.data, compress=True)
            topic_msg.data = shared_memory.object_id_to_bytes(plasma_obj_id)
        else:
            raise NotImplementedError

        if trace is not None:
            profiler.touch_trace(trace, self.tagged_publish_topic)
            profiler.copy_trace(trace, topic_msg)

        await self.producer.send(
            self.publish_topic.name,
            value=topic_msg.SerializeToString(),
            key=msg.source,
        )

    async def _read(self) -> AsyncGenerator[List[ConsumerRecord], None]:
        topic_messages = {topic: Queue() for topic in self.source_topics}
        async for record in self.consumer:
            queue = topic_messages[record.topic]
            queue.put(record)
            if all([not queue.empty() for queue in topic_messages.values()]):
                records = [queue.get() for queue in topic_messages.values()]
                yield records

    async def _read(self) -> AsyncGenerator[List[ConsumerRecord], None]:
        topic_messages: Dict[str, Queue] = {
            topic: Queue() for topic in self.source_topics
        }
        async for record in self.consumer:
            queue = topic_messages[record.topic]
            queue.put(record)
            if all([not queue.empty() for queue in topic_messages.values()]):
                records = [queue.get() for queue in topic_messages.values()]
                yield records

    async def _parse(self, msg: str) -> Awaitable[Message]:
        topic_msg = TopicMessage.FromString(msg)
        topic = self.topic_registry[topic_msg.type_name]

        data = None
        if topic.data_location == DataLocation.MESSAGE:
            data = topic.type.FromString(topic.data)
        elif topic.data_location == DataLocation.CPU:
            raise NotImplementedError
        elif topic.data_location == DataLocation.GPU:
            raise NotImplementedError
        elif topic.data_location == DataLocation.CPU_NDARRAY:
            plasma_object_id = shared_memory.object_id_from_bytes(topic_msg.data)
            data = self.shm_client.read(plasma_object_id)
        elif topic.data_location == DataLocation.GPU_NDARRAY:
            raise NotImplementedError

        return topic, topic_msg, data

    async def process(
        self,
        inputs: List[Message],
    ) -> Awaitable[Optional[NewMessage]]:
        raise NotImplementedError

    async def run(
        self,
        start_ts: Optional[int] = None,
        end_ts: Optional[int] = None,
        profile: Optional[bool] = False,
    ) -> None:
        if start_ts is not None:
            pass

        async for records in self._read():
            inputs = await asyncio.gather(
                *[self._parse(record.value) for record in records]
            )
            output_msg = await self.process(inputs)
            if output_msg is not None:
                await self._publish(output_msg)
            if end_ts is not None and inputs[0].timestamp >= end_ts:
                break

    def register(self, process_fn: Callable[List[Message]]):
        def decorated_fn(self, fn, inputs):
            return fn(inputs)

        self.process = partial(decorated_fn, self, process_fn)

    def mainloop(
        self,
        start_ts: Optional[int] = None,
        end_ts: Optional[int] = None,
        profile: Optional[bool] = False,
    ) -> Process:
        def process():
            async def exec():
                async with self as node:
                    await node.run(start_ts, end_ts, profile)

            uvloop.install()
            asyncio.run(exec())

        p = Process(target=process)
        p.start()
        return p
