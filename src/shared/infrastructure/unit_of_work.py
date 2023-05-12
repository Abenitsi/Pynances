from typing import Any

from src.shared.application.unit_of_work import UnitOfWork
from src.shared.domain.connection import ConnectionFactory
from src.shared.infrastructure.connection import SQLAlchemyConnection


class SQLAlchemyUnitOfWork(UnitOfWork):
    connection: SQLAlchemyConnection

    def __init__(
        self,
        connection_factory: ConnectionFactory,
    ) -> None:
        self.connection_factory = connection_factory

    def __enter__(self) -> None:
        self.connection = self.connection_factory.make(SQLAlchemyConnection)

    def __exit__(self, *args: Any) -> None:
        super().__exit__(*args)
        self.connection.close()

    def commit(self) -> None:
        self.connection.commit()

    def rollback(self) -> None:
        self.connection.rollback()
