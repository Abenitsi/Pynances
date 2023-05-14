import json
from typing import Any, Optional, Type

from sqlalchemy import Dialect
from sqlalchemy.sql.type_api import _T
from sqlalchemy.types import Float, Integer, String, TypeDecorator, Text

from src.shared.domain.domain_event import (
    DomainEvent,
    DomainEventId,
    DomainEventRepository,
)
from src.shared.infrastructure.connection import SQLAlchemyConnection
from src.shared.infrastructure.exception import ModelNotFound


class GenericDecorator(TypeDecorator):  # type: ignore
    t: type
    parent_t: type

    def __init__(self, t: type):
        super().__init__()
        self.t = t
        self.parent_t = t.mro()[-2]

    def process_bind_param(self, value: object, dialect: Any) -> Any:
        if value is not None:
            if self.parent_t == dict:
                return json.dumps(value)
            return self.parent_t(value)

    def process_result_value(self, value: Any, dialect: Any) -> Any:
        if value is not None:
            if self.parent_t == dict:
                return value
            return self.t(value)

    def process_literal_param(
        self, value: Optional[_T], dialect: Dialect
    ) -> str:
        return str(value)

    @property
    def python_type(self) -> Type[Any]:
        return self.parent_t


def type_decorator_factory(
    t: type, cache_ok: bool | None = None
) -> GenericDecorator:
    def sqlalchemy_type_picker(t: type) -> Any:
        if t == int:
            return Integer
        if t == float:
            return Float
        if t == dict:
            return Text
        return String

    GenericDecorator.impl = sqlalchemy_type_picker(t.mro()[-2])
    GenericDecorator.cache_ok = cache_ok
    return GenericDecorator(t)


class SqlAlchemyEventRepository(DomainEventRepository):
    connection: SQLAlchemyConnection

    def __init__(self, connection: SQLAlchemyConnection) -> None:
        self.connection = connection

    def get(self, id: DomainEventId) -> DomainEvent:
        events = self.connection.read(DomainEvent, DomainEvent.id == id)
        event: DomainEvent = events[0]
        return event

    def store(self, domain_event: DomainEvent) -> None:
        self.connection.write(domain_event)

    def all(self) -> list[DomainEvent]:
        pass


class InMemoryEventRepository(DomainEventRepository):
    domain_events: list[DomainEvent] = []

    def get(self, id: DomainEventId) -> DomainEvent:
        for domain_event in self.domain_events:
            if domain_event.id == id:
                return domain_event

        raise ModelNotFound(f"domain event with id {id} does not exist")

    def store(self, *domain_events: DomainEvent) -> None:
        self.domain_events += domain_events

    def all(self) -> list[DomainEvent]:
        return self.domain_events
