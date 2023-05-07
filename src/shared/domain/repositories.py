from abc import ABC, abstractmethod
from typing import Type, Any

from src.shared.domain.aggregate_root import AggregateRoot


class Connection(ABC):
    @abstractmethod
    def write(self, aggregate: AggregateRoot) -> None:
        pass

    @abstractmethod
    def read(self, aggregate: Type[AggregateRoot], *filters: Any) -> AggregateRoot:
        pass


class Repository(ABC):
    connection: Connection

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    @abstractmethod
    def save(self, aggregate: AggregateRoot) -> None:
        pass
