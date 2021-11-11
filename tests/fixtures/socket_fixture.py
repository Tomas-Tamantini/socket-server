import pytest

from typing import Callable, List, Optional


class MockSocket:
    index = 0

    def __init__(self, requests: List[str]):
        self.__requests = requests
        self.__hashable_key = MockSocket.index
        MockSocket.index += 1
        self.received_notifications = []

    async def send(self, msg: str) -> None:
        self.received_notifications.append(msg)

    def __hash__(self) -> int:
        return self.__hashable_key

    def __aiter__(self):
        return self

    async def __anext__(self):
        if len(self.__requests) == 0:
            raise StopAsyncIteration
        else:
            return self.__requests.pop(0)


@pytest.fixture()
def socket_factory() -> Callable[..., MockSocket]:
    def make_socket(requests: Optional[List[str]] = None) -> MockSocket:
        if requests is None:
            requests = []
        return MockSocket(requests)
    return make_socket
