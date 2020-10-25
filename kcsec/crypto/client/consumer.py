import traceback
from abc import ABC
from abc import abstractmethod


class Consumer(ABC):
    def __init__(self, connection, *args, **kwargs):
        self.conn = connection

    async def __aenter__(self) -> "Consumer":
        await self.subscribe()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        traceback.print_exc()
        await self.unsubscribe()

    def __await__(self):
        return self.__aenter__().__await__()

    @classmethod
    @abstractmethod
    async def connect(cls, url) -> "Consumer":
        pass

    @abstractmethod
    async def subscribe(self, *args, **kwargs):
        return

    @abstractmethod
    async def handle_message(self, message):
        pass

    @abstractmethod
    async def unsubscribe(self, *args, **kwargs):
        pass
