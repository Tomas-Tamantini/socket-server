from typing import Generator, Hashable, Protocol, Tuple


class Producer(Protocol):
    @property
    async def notifications(self) -> Generator[Tuple[Hashable, str], None, None]:
        """Async generatod that yields tuples with (recipient client, message)"""