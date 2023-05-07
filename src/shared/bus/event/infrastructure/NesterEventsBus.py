from src.shared.bus.event.domain.DomainEvent import DomainEvent
from src.shared.bus.event.domain.EventBus import EventBus


class NesterEventsBus(EventBus):
    def publish(self, domain_event: DomainEvent) -> None:
        pass
