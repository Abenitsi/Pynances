from abc import ABC
from src.account.domain.repository import AccountRepository
from src.account.infrastructure.repository import SQLAlchemyAccountRepository
from src.shared.application.unit_of_work import UnitOfWork
from src.shared.domain.domain_event import DomainEventRepository
from src.shared.infrastructure.repository import SqlAlchemyEventRepository
from src.shared.infrastructure.unit_of_work import SQLAlchemyUnitOfWork


class AccountUoW(UnitOfWork, ABC):
    accounts: AccountRepository


class SQLAlchemyAccountUoW(SQLAlchemyUnitOfWork, ABC):
    accounts: AccountRepository
    events: DomainEventRepository

    def __enter__(self) -> None:
        super().__enter__()
        self.accounts = SQLAlchemyAccountRepository(self.connection)
        self.events = SqlAlchemyEventRepository(self.connection)

    def commit(self) -> None:
        for accounts in self.accounts.seen:
            for event in accounts.pull_events():
                self.events.store(event)
        super().commit()
