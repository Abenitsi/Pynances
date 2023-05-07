from abc import ABC, abstractmethod
from typing import Any

from src.shared.domain.domain_event import DomainEvent


class Entity(ABC):
    def dict(self) -> dict[str, Any]:
        return self.__dict__


class AggregateRoot(Entity):
    __events: list[DomainEvent] = []

    @abstractmethod
    def __init__(self) -> None:
        pass

    def record(self, event: DomainEvent) -> None:
        self.__events.append(event)

    def pull_events(self) -> list[DomainEvent]:
        events = self.__events
        self.__events = []
        return events
