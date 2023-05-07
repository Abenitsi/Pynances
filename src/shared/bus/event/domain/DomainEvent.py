from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from src.shared.bus.event.domain.EventId import EventId


class DomainEvent(ABC):
    def __init__(
        self,
        data: Any,
        event_id: EventId = EventId.rand(),
        occurred_at: datetime = datetime.now(),
    ):
        self.__id = event_id
        self.__occurred_at = occurred_at
        self.__data = data

    def id(self) -> EventId:
        return self.__id

    def occurred_at(self) -> datetime:
        return self.__occurred_at

    @abstractmethod
    def data(self) -> Any:
        pass
