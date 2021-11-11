import pytest
from socket_server.server_engine import ServerEngine
from socket_server.socket_manager import SocketManager
from typing import Hashable


class MockConsumer:
    def __init__(self) -> None:
        self.received_requests = []

    async def handle_message(self, _: Hashable, message: str) -> None:
        self.received_requests.append(message)

    async def handle_client_connected(self, user_id: Hashable) -> None:
        pass

    async def handle_client_disconnected(self, user_id: Hashable) -> None:
        pass


@pytest.mark.asyncio
async def test_messages_are_passed_to_consumer(socket_factory):
    consumer = MockConsumer()
    server = ServerEngine(SocketManager(), consumer)
    sample_requests = ['hello', 'another request', 'yet another request']
    stored_requests = sample_requests[:]
    socket = socket_factory(requests=sample_requests)
    await server.run_consumer(socket)
    assert consumer.received_requests == stored_requests
