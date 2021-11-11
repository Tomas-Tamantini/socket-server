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


def test_ids_should_be_unique(socket_factory):
    manager = SocketManager()
    socket_a = socket_factory()
    id_a = manager.register(socket_a)
    socket_b = socket_factory()
    id_b = manager.register(socket_b)
    assert id_a != id_b


def test_get_socket(socket_factory):
    manager = SocketManager()
    socket = socket_factory()
    user_id = manager.register(socket)
    assert manager.get_socket(user_id) == socket


def test_unregister_socket(socket_factory):
    manager = SocketManager()
    socket = socket_factory()
    user_id = manager.register(socket)
    manager.unregister(user_id)
    assert manager.num_clients == 0
