from abc import ABC, abstractmethod
from src.shared.bus.event.domain.DomainEvent import DomainEvent
from typing import Any


class EventSubscriber(ABC):
    @abstractmethod
    def subscribed_to(self) -> list[DomainEvent]:
        pass

    @abstractmethod
    def handle(self) -> Any:
        pass
