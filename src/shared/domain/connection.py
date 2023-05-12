from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar

from src.shared.domain.aggregate_root import AggregateRoot


class ConnectionConfig(ABC):
    @abstractmethod
    def uri(self) -> str:
        pass


class Connection(ABC):
    @abstractmethod
    def __init__(self, config: ConnectionConfig) -> None:
        pass

    @abstractmethod
    def write(self, aggregate: AggregateRoot) -> None:
        pass

    @abstractmethod
    def read(
        self, aggregate: Type[AggregateRoot], *filters: Any
    ) -> AggregateRoot:
        pass


T = TypeVar("T", bound=Connection)


class ConnectionFactory:
    def __init__(self, connection_config: ConnectionConfig) -> None:
        self.connection_config = connection_config

    def make(self, connection_type: Type[T]) -> T:
        return connection_type(self.connection_config)
