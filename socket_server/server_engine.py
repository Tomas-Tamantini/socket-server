import logging
from typing import Optional

from .consumer import Consumer
from .producer import Producer
from .socket_manager import SocketManager

from websockets import ConnectionClosedError, ConnectionClosedOK, ConnectionClosed

DISCONNECT_EXCEPTIONS = (ConnectionClosedError,
                         ConnectionClosedOK, ConnectionClosed)


class ServerEngine:
    def __init__(self, socket_manager: SocketManager, consumer: Optional[Consumer] = None, producer: Optional[Producer] = None):
        self.__socket_manager = socket_manager
        self.__consumer = consumer
        self.__producer = producer

    async def run_consumer(self, socket):
        try:
            async for request in socket:
                await self.__handle_request(socket, request)
        except DISCONNECT_EXCEPTIONS:
            await self.__unregister_socket(socket)
        finally:
            await self.__unregister_socket(socket)

    async def run_producer(self):
        if self.__producer is None:
            return
        async for user_id, message in self.__producer.notifications:
            socket = self.__socket_manager.get_socket(user_id)
            if socket is not None:
                await self.__send_message(socket, message)

    async def __handle_request(self, socket, request: str) -> None:
        client_id = self.__socket_manager.get_client_id(socket)
        if client_id is None:
            client_id = self.__socket_manager.register(socket)
            logging.info(f'New client registered with ID: {client_id}')
            if self.__consumer is not None:
                await self.__consumer.handle_client_connected(client_id)

        if self.__consumer is not None:
            await self.__consumer.handle_message(client_id, request)

    async def __unregister_socket(self, socket) -> None:
        client_id = self.__socket_manager.get_client_id(socket)
        if client_id is None:
            return
        if self.__consumer is not None:
            await self.__consumer.handle_client_disconnected(client_id)
        self.__socket_manager.unregister(client_id)
        logging.info(f'Client with ID: {client_id} disconnected')

    async def __send_message(self, socket, message: str) -> None:
        try:
            await socket.send(message)
        except DISCONNECT_EXCEPTIONS:
            await self.__unregister_socket(socket)
