import asyncio
from functools import partial
from typing import Optional

import websockets

from .consumer import Consumer
from .producer import Producer
from .server_engine import ServerEngine
from .socket_manager import SocketManager


async def run_server(host_address: str = 'localhost', port: int = 8080,
                     consumer: Optional[Consumer] = None, producer: Optional[Producer] = None):
    """
    Runs server at given host address and port.
    :param consumer: Handles incoming messages from the clients
    :param producer: Produces outgoing messages to the clients. If not provided, and consumer is provided, 
                     and consumer implements Producer interface, then consumer will be used as producer.
    """
    server_engine = _initialize_server_engine(consumer, producer)
    async with websockets.serve(partial(_gather_tasks, server_engine=server_engine), host_address, port):
        await asyncio.Future()


def _initialize_server_engine(consumer: Optional[Consumer], producer: Optional[Producer]) -> ServerEngine:
    if consumer is not None and producer is None and isinstance(consumer, Producer):
        producer = consumer
    socket_manager = SocketManager()
    return ServerEngine(socket_manager, consumer, producer)


async def _gather_tasks(socket, path, server_engine: ServerEngine):
    consumer_task = asyncio.ensure_future(server_engine.run_consumer(socket))
    producer_task = asyncio.ensure_future(server_engine.run_producer())
    _, pending = await asyncio.wait([consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()
