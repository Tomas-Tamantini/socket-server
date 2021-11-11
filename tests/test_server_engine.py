from typing import Hashable, List, Tuple, Generator

import pytest
from socket_server.server_engine import ServerEngine
from socket_server.socket_manager import SocketManager


class MockConsumer:
    def __init__(self) -> None:
        self.received_requests = []

    async def handle_message(self, _: Hashable, message: str) -> None:
        self.received_requests.append(message)

    async def handle_client_connected(self, user_id: Hashable) -> None:
        pass

    async def handle_client_disconnected(self, user_id: Hashable) -> None:
        pass


class MockProducer:
    def __init__(self, notifications: List[Tuple[Hashable, str]]) -> None:
        self.__notifications = notifications

    @property
    async def notifications(self) -> Generator[Tuple[Hashable, str], None, None]:
        for n in self.__notifications:
            yield n


@pytest.mark.asyncio
async def test_messages_are_passed_to_consumer(socket_factory):
    consumer = MockConsumer()
    server = ServerEngine(SocketManager(), consumer)
    sample_requests = ['hello', 'another request', 'yet another request']
    stored_requests = sample_requests[:]
    socket = socket_factory(requests=sample_requests)
    await server.run_consumer(socket)
    assert consumer.received_requests == stored_requests


@pytest.mark.asyncio
async def test_notifications_are_sent_to_proper_sockets(socket_factory):
    socket_manager = SocketManager()
    socket_a = socket_factory()
    user_a = socket_manager.register(socket_a)
    socket_b = socket_factory()
    user_b = socket_manager.register(socket_b)
    notifications = [(user_a, 'first_msg_to_a'),
                     (user_b, 'first_msg_to_b'), (user_a, 'second_msg_to_a')]
    producer = MockProducer(notifications)
    server = ServerEngine(socket_manager, producer=producer)
    await server.run_producer()
    assert socket_a.received_notifications == [
        'first_msg_to_a', 'second_msg_to_a']
    assert socket_b.received_notifications == ['first_msg_to_b']
