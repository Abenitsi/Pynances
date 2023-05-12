from src import CoreConfig
from src.shared.dependency_container import DependencyContainer
from src.account.domain.model import Account
from src.account.application.use_case import Create as CreateAccount


class AccountSDKContext:
    __container: DependencyContainer

    def __init__(self, container: DependencyContainer) -> None:
        self.__container = container

    def create(self) -> Account:
        return self.__container.get(CreateAccount)()


class SDK:
    container = DependencyContainer.get_container()

    def __init__(self, config: CoreConfig) -> None:
        self.config = config
        self.__bootstrap()
        self.account = self.container.get(AccountSDKContext)

    def __bootstrap(self) -> None:
        for key, value in self.config.bindings.items():
            self.container.set(key, value(self))
