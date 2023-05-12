from dataclasses import dataclass

from src import AccountUoW
from src.account.domain.model import (
    Account,
    AccountId,
    AccountName,
    AccountIban,
    AccountHash,
    AccountType,
    AccountAmount,
)
from src.shared.application.use_case import UseCase


@dataclass
class Create(UseCase):
    uow: AccountUoW

    def __call__(self) -> Account:
        with self.uow:
            account = Account(
                id=AccountId.rand(),
                name=AccountName("Cuenta"),
                iban=AccountIban("Iban"),
                hash=AccountHash("hash"),
                type=AccountType("regular"),
                amount=AccountAmount(0),
            )
            self.uow.accounts.save(account)
            self.uow.commit()
            return account
