from socket_server.socket_manager import SocketManager


def test_manager_starts_empty():
    manager = SocketManager()
    assert manager.num_clients == 0
