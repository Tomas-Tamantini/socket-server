import pytest
from socket_server.socket_manager import SocketManager


def test_manager_starts_empty():
    manager = SocketManager()
    assert manager.num_clients == 0


def test_socket_can_register(socket_factory):
    manager = SocketManager()
    socket = socket_factory()
    manager.register(socket)
    assert manager.num_clients == 1


def test_same_socket_cannot_register_twice(socket_factory):
    manager = SocketManager()
    socket = socket_factory()
    manager.register(socket)
    with pytest.raises(SocketManager.SocketAlreadyRegisteredError):
        manager.register(socket)
