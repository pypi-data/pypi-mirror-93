import asyncio

from typing import (
    Awaitable,
    List,
    Optional,
)

from metta.common import profiler
from metta.common.topics import Topic, NewMessage
from metta.nodes.node import Node
from metta.proto.topic_pb2 import DataLocation


class SourceNode(Node):
    def __init__(
        self,
        *,
        publish_topic: Topic,
        kafka_brokers: List[str],
        zookeeper_hosts: List[str],
        event_loop: Optional[asyncio.unix_events._UnixSelectorEventLoop] = None,
    ):
        super().__init__(
            publish_topic=publish_topic,
            kafka_brokers=kafka_brokers,
            zookeeper_hosts=zookeeper_hosts,
            event_loop=event_loop,
        )

    async def _process(
        self,
        profile: bool = False,
    ) -> Optional[NewMessage]:
        output_msg = await self.process()
        if output_msg is not None and profile:
            trace = profiler.init_trace()
            profiler.touch_trace(trace, self.publish_topic)
            output_msg.trace = trace
        return output_msg

    async def process(self) -> Optional[NewMessage]:
        raise NotImplementedError

    async def run(
        self,
        start_ts: Optional[int] = None,
        end_ts: Optional[int] = None,
        profile: Optional[bool] = False,
    ) -> None:
        while True:
            output_msg = await self._process()
            if output_msg is not None:
                await self._publish(output_msg)
