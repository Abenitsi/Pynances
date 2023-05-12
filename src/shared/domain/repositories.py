from abc import ABC, abstractmethod

from src.shared.domain.aggregate_root import AggregateRoot
from src.shared.domain.connection import Connection


class Repository(ABC):
    connection: Connection

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    @abstractmethod
    def save(self, aggregate: AggregateRoot) -> None:
        pass
