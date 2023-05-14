from src.account.application.use_case import Create as CreateAccount
from src.shared.dependency_container import DependencyContainer
from src.account.application.use_case import CreateData


class AccountSDKContext:
    __container: DependencyContainer

    def __init__(self, container: DependencyContainer) -> None:
        self.__container = container

    def create(self, name: str, iban: str, amount: float, type: str) -> None:
        data = CreateData(
            name=name,
            iban=iban,
            amount=amount,
            type=type,
        )
        self.__container.get(CreateAccount)(data=data)
