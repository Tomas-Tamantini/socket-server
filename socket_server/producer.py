from typing import Generator, Hashable, Protocol, Tuple, runtime_checkable


@runtime_checkable
class Producer(Protocol):
    @property
    async def notifications(self) -> Generator[Tuple[Hashable, str], None, None]:
        """Async generator that yields tuples with (recipient client, message)"""
