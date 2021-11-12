from typing import Hashable, Protocol


class Consumer(Protocol):
    async def handle_message(self, client_id: Hashable, message: str) -> None:
        """Handle incoming message from client"""

    async def handle_client_connected(self, client_id: Hashable) -> None:
        ...

    async def handle_client_disconnected(self, client_id: Hashable) -> None:
        ...
