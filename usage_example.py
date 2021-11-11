import asyncio
import logging
from random import choice
from typing import Generator, Hashable, Tuple

from socket_server import run_server


logging.basicConfig(level=logging.INFO)

"""
Options for consumer/producer:
    - There can be just one object, which implements both protocols.
    - There can be two separate objects, one consumer and one producer.
    - There can be just a consumer
    - There can be just a producer
    - There can be neither (although that wouldn't be a very interesting server)

In the example below, the first option was chosen.
"""


class ConsumerProducer:
    def __init__(self) -> None:
        self.__clients = set()
    # Consumer protocol methods

    async def handle_message(self, user_id: Hashable, message: str) -> None:
        print(f'Received a message from {user_id}: {message}')

    async def handle_client_connected(self, user_id: Hashable) -> None:
        self.__clients.add(user_id)

    async def handle_client_disconnected(self, user_id: Hashable) -> None:
        if user_id in self.__clients:
            self.__clients.remove(user_id)

    # Producer protocol methods
    @property
    async def notifications(self) -> Generator[Tuple[Hashable, str], None, None]:
        """Send 'Hello!' to some random client every second"""
        while True:
            await asyncio.sleep(1)
            if len(self.__clients) == 0:
                continue
            user_id = choice(list(self.__clients))
            print(f'Sending "hello" to client {user_id}')
            yield (user_id, 'Hello!')


async def main():
    await run_server('localhost',  8080, ConsumerProducer())

if __name__ == '__main__':
    asyncio.run(main())
