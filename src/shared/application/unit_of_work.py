from abc import ABC, abstractmethod
from typing import Any


class UnitOfWork(ABC):
    @abstractmethod
    def __enter__(self) -> int:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass

    def __exit__(self, *args: Any) -> None:
        self.rollback()
