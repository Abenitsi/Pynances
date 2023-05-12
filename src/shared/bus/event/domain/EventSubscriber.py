from abc import ABC, abstractmethod
from typing import Any

from src.shared.bus.event.domain.DomainEvent import DomainEvent


class EventSubscriber(ABC):
    @abstractmethod
    def subscribed_to(self) -> list[DomainEvent]:
        pass

    @abstractmethod
    def handle(self) -> Any:
        pass
