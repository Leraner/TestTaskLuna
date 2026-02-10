from abc import ABC, abstractmethod


class BaseSeeder(ABC):
    @abstractmethod
    async def seed(self) -> None:
        pass

    @abstractmethod
    async def clear(self) -> None:
        pass
