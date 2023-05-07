from abc import ABC, abstractmethod
from src.shared.bus.event.domain.DomainEvent import DomainEvent


class EventBus(ABC):
    @abstractmethod
    def publish(self, domain_event: DomainEvent) -> None:
        pass
