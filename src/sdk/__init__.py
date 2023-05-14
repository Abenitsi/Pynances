from src import CoreConfig
from src.account.application.unit_of_work import (
    AccountUoW,
    SQLAlchemyAccountUoW,
)
from src.shared.domain.connection import ConnectionConfig
from src.shared.dependency_container import DependencyContainer
from src.shared.domain.domain_event import DomainEventRepository
from src.shared.infrastructure.connection import (
    PostgreSQLAlchemyConnectionConfig,
)
import src.sdk.contexts as contexts
from src.shared.infrastructure.repository import SqlAlchemyEventRepository


class SDK:
    __container = DependencyContainer.get_container()

    def __init__(self, config: CoreConfig) -> None:
        self.__config = config
        self.__bootstrap()
        # ------------------- CUT HERE ------------------- #
        self.account = self.__container.get(contexts.AccountSDKContext)
        # ------------------- CUT HERE ------------------- #

    def __bootstrap(self) -> None:
        self.__container.set(
            ConnectionConfig,
            PostgreSQLAlchemyConnectionConfig(
                user=self.__config.db_user,
                password=self.__config.db_password,
                host=self.__config.db_host,
                db_name=self.__config.db_name,
            ),
        )
        self.__container.set(
            AccountUoW, self.__container.get(SQLAlchemyAccountUoW)
        )
        self.__container.set(DependencyContainer, self.__container)
