from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.shared.domain.valueobject import ULIDValueObject


class DomainEventId(ULIDValueObject):
    pass


@dataclass(frozen=True, kw_only=True)
class DomainEvent:
    id: DomainEventId
    data: Any
    occurred_at: datetime = datetime.now()


@dataclass(frozen=True, kw_only=True)
class UserCreatedEvent(DomainEvent):
    data: int


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
