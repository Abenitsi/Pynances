from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from src.shared.domain.valueobject import (
    TimestampValueObject,
    DictValueObject,
    NonEmptyStringValueObject,
    UUIDValueObject,
)


class DomainEventId(UUIDValueObject):
    pass


class DomainEventOccurredAt(TimestampValueObject):
    pass


class DomainEventData(DictValueObject):
    pass


class DomainEventName(NonEmptyStringValueObject):
    pass


@dataclass
class DomainEvent:
    id: DomainEventId
    name: DomainEventName
    occurred_at: DomainEventOccurredAt
    data: DomainEventData

    @classmethod
    def register(cls, data: dict):
        return cls(
            id=DomainEventId.rand(),
            name=DomainEventName(cls.__module__ + "." + cls.__name__),
            occurred_at=DomainEventOccurredAt(datetime.now().timestamp()),
            data=DomainEventData(data),
        )


class DomainEventRepository(ABC):
    @abstractmethod
    def get(self, id: DomainEventId) -> DomainEvent:
        pass

    @abstractmethod
    def store(self, domain_event: DomainEvent) -> None:
        pass

    @abstractmethod
    def all(self) -> list[DomainEvent]:
        pass
