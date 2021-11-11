import pytest

from typing import Callable


class MockSocket:
    index = 0

    def __init__(self):
        self.__hashable_key = MockSocket.index
        MockSocket.index += 1

    def __hash__(self) -> int:
        return self.__hashable_key


@pytest.fixture()
def socket_factory() -> Callable[..., MockSocket]:
    def make_socket() -> MockSocket:
        return MockSocket()
    return make_socket
