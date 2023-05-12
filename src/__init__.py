from dataclasses import dataclass

from src.account.application.unit_of_work import (
    SQLAlchemyAccountUoW,
    AccountUoW,
)
from src.shared.dependency_container import DependencyContainer
from src.shared.domain.connection import ConnectionConfig
from src.shared.infrastructure.connection import (
    PostgreSQLAlchemyConnectionConfig,
)


@dataclass(frozen=True, kw_only=True)
class CoreConfig:
    # DB config
    db_driver: str
    db_user: str
    db_password: str
    db_host: str
    db_name: str

    # Cache config

    # Binding
    bindings = {
        ConnectionConfig: lambda self: PostgreSQLAlchemyConnectionConfig(
            user=self.config.db_user,
            password=self.config.db_password,
            host=self.config.db_host,
            db_name=self.config.db_name,
        ),
        AccountUoW: lambda self: SQLAlchemyAccountUoW,
        DependencyContainer: lambda self: self.container,
    }
