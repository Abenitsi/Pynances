from src.account.application.use_case import CreateData
from src.shared.dependency_container import DependencyContainer
from src.account.application.use_case import Create as CreateAccount


class AccountSDKContext:
    __container: DependencyContainer

    def __init__(self, container: DependencyContainer) -> None:
        self.__container = container

    def create(
        self, name: str, iban: str, hash: str, amount: float, type: str
    ) -> None:
        data = CreateData(
            name=name,
            iban=iban,
            hash=hash,
            amount=amount,
            type=type,
        )
        self.__container.get(CreateAccount)(data=data)
