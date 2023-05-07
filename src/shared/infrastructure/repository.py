from typing import Any, Type, TypeVar, Optional

from sqlalchemy import create_engine, Dialect
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql.type_api import _T, TypeEngine
from sqlalchemy.types import TypeDecorator, String, Integer, Float

from src.shared.domain.aggregate_root import AggregateRoot
from src.shared.domain.domain_event import (
    DomainEvent,
    DomainEventId,
    DomainEventRepository,
)
from src.shared.domain.repositories import Connection
from src.shared.infrastructure.exception import ModelNotFound

T = TypeVar("T", bound=AggregateRoot)


class SqlAlchemyConnection(Connection):
    def __init__(
        self, *, driver: str, user: str, password: str, host: str, db_name: str
    ):
        self.connection = Session(
            create_engine(
                driver + "://" + user + ":" + password + "@" + host + "/" + db_name
            )
        )

    def write(self, aggregate: T) -> None:
        self.connection.add(aggregate)

    def read(self, aggregate: Type[T], *filters: Any) -> Query[T]:
        return self.connection.query(aggregate).filter(*filters)

    def begin_transaction(self) -> Any:
        return self.connection.begin()

    def commit(self) -> None:
        self.connection.commit()


class GenericDecorator(TypeDecorator):  # type: ignore
    t: type
    parent_t: type

    def __init__(self, t: type):
        super().__init__()
        self.t = t
        self.parent_t = t.mro()[-2]

    def process_bind_param(self, value: object, dialect: Any) -> Any:
        if value is not None:
            return self.parent_t(value)

    def process_result_value(self, value: Any, dialect: Any) -> Any:
        if value is not None:
            return self.t(value)

    def process_literal_param(self, value: Optional[_T], dialect: Dialect) -> str:
        return str(value)

    @property
    def python_type(self) -> Type[Any]:
        return self.parent_t


def type_decorator_factory(t: type, cache_ok: bool | None = None) -> GenericDecorator:
    def sqlalchemy_type_picker(t: type) -> Any:
        if t == int:
            return Integer
        if t == float:
            return Float
        return String

    GenericDecorator.impl = sqlalchemy_type_picker(t.mro()[-2])
    GenericDecorator.cache_ok = cache_ok
    return GenericDecorator(t)


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
