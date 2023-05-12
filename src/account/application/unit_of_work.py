from abc import ABC
from src.account.domain.repository import AccountRepository
from src.account.infrastructure.repository import SQLAlchemyAccountRepository
from src.shared.application.unit_of_work import UnitOfWork
from src.shared.infrastructure.unit_of_work import SQLAlchemyUnitOfWork


class AccountUoW(UnitOfWork, ABC):
    accounts: AccountRepository


class SQLAlchemyAccountUoW(SQLAlchemyUnitOfWork, ABC):
    accounts: AccountRepository

    def __enter__(self) -> None:
        super().__enter__()
        self.accounts = SQLAlchemyAccountRepository(self.connection)
