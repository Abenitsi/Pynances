from dataclasses import dataclass

from src.account.application.unit_of_work import AccountUoW
from src.account.domain.model import (
    Account,
    AccountName,
    AccountIban,
    AccountHash,
    AccountType,
    AccountAmount,
)
from src.shared.application.use_case import UseCase


@dataclass(frozen=True)
class CreateData:
    name: str
    iban: str
    hash: str
    amount: float
    type: str

    def account(self) -> Account:
        return Account.create(
            name=AccountName(self.name),
            iban=AccountIban(self.iban),
            hash=AccountHash(self.hash),
            type=AccountType(self.type),
            amount=AccountAmount(self.amount),
        )


@dataclass
class Create(UseCase):
    uow: AccountUoW

    def __call__(self, data: CreateData) -> None:
        with self.uow:
            account = data.account()
            self.uow.accounts.save(account)
            self.uow.commit()
