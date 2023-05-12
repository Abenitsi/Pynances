from dataclasses import dataclass
from typing import Any, Type, TypeVar

from sqlalchemy import create_engine
from sqlalchemy.orm import Query, Session

from src.shared.domain.aggregate_root import AggregateRoot
from src.shared.domain.connection import Connection, ConnectionConfig

T = TypeVar("T", bound=AggregateRoot)


@dataclass(frozen=True)
class PostgreSQLAlchemyConnectionConfig(ConnectionConfig):
    driver = "postgresql"
    user: str
    password: str
    host: str
    db_name: str

    def uri(self) -> str:
        return (
            self.driver
            + "://"
            + self.user
            + ":"
            + self.password
            + "@"
            + self.host
            + "/"
            + self.db_name
        )


class SQLAlchemyConnection(Connection):
    _connection: Session

    def __init__(self, db_config: ConnectionConfig):
        self._connection = Session(create_engine(db_config.uri()))

    def write(self, aggregate: T) -> None:
        self._connection.add(aggregate)

    def read(self, aggregate: Type[T], *filters: Any) -> Query[T]:
        return self._connection.query(aggregate).filter(*filters)

    def begin_transaction(self) -> Any:
        return self._connection.begin()

    def commit(self) -> None:
        self._connection.commit()

    def rollback(self) -> None:
        self._connection.rollback()

    def close(self) -> None:
        self._connection.close()
