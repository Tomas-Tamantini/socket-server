from typing import Hashable


class SocketManager:
    def __init__(self) -> None:
        self.__current_id = 0
        self.__sockets_to_ids = {}
        self.__ids_to_sockets = {}

    @property
    def num_clients(self) -> int:
        return len(self.__sockets_to_ids)

    def register(self, socket) -> Hashable:
        if socket in self.__sockets_to_ids:
            raise self.SocketAlreadyRegisteredError(
                socket, self.__sockets_to_ids[socket])
        new_id = self.__current_id
        self.__sockets_to_ids[socket] = new_id
        self.__ids_to_sockets[new_id] = socket
        self.__current_id += 1
        return new_id

    def unregister(self, client_id: Hashable):
        if client_id not in self.__ids_to_sockets:
            raise self.SocketNotRegisteredError(client_id)
        socket = self.__ids_to_sockets.pop(client_id)
        del self.__sockets_to_ids[socket]

    def get_socket(self, client_id: Hashable):
        return self.__ids_to_sockets.get(client_id)

    # Exceptions:

    class SocketAlreadyRegisteredError(Exception):
        def __init__(self, socket, socket_id) -> None:
            msg = f"Socket with id {socket_id} is already registered - {str(socket)}"
            super().__init__(msg)

    class SocketNotRegisteredError(Exception):
        def __init__(self, socket_id) -> None:
            msg = f"Socket with id {socket_id} is not registered"
            super().__init__(msg)
