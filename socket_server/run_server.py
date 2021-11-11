import asyncio
from functools import partial
from typing import Optional

import websockets

from .consumer import Consumer
from .producer import Producer

async def run_server(host_address: str = 'localhost', port: int = 8080,
                     consumer: Optional[Consumer] = None, producer: Optional[Producer] = None):
    """
    Runs server at given host address and port.
    :param consumer: Handles incoming messages from the clients
    :param producer: Produces outgoing messages to the clients
    """
    async with websockets.serve(partial(_gather_tasks, consumer=consumer, producer=producer), host_address, port):
        await asyncio.Future()


async def _gather_tasks(socket, path, consumer: Optional[Consumer], producer: Optional[Producer]):
    consumer_task = asyncio.ensure_future(_consumer_handler(socket, consumer))
    producer_task = asyncio.ensure_future(_producer_handler(socket, producer))
    _, pending = await asyncio.wait([consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()


async def _consumer_handler(socket, consumer: Optional[Consumer]):
    pass


async def _producer_handler(socket, producer: Optional[Producer]):
    pass
