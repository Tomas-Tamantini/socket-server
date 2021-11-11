class SocketManager:
    def __init__(self) -> None:
        self.__current_id = 0
        self.__sockets_to_ids = {}
        self.__ids_to_sockets = {}

    @property
    def num_clients(self) -> int:
        return len(self.__sockets_to_ids)

    def register(self, socket) -> None:
        if socket in self.__sockets_to_ids:
            raise self.SocketAlreadyRegisteredError(socket, self.__sockets_to_ids[socket])
        self.__sockets_to_ids[socket] = self.__current_id
        self.__ids_to_sockets[self.__current_id] = socket
        self.__current_id += 1

    # Exceptions:

    class SocketAlreadyRegisteredError(Exception):
        def __init__(self, socket, socket_id) -> None:
            msg = f"Socket with id {socket_id} is already registered - {str(socket)}"
            super().__init__(msg)
