from abc import ABC, abstractmethod
from src.account.domain.model import Account, AccountId
from src.shared.domain.repositories import Repository


class AccountRepository(Repository, ABC):
    @abstractmethod
    def save(self, account: Account) -> None:
        pass

    @abstractmethod
    def get(self, account_id: AccountId) -> Account:
        pass
