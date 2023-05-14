from dataclasses import dataclass

from src.account.domain.events import AccountCreated
from src.shared.domain.aggregate_root import AggregateRoot
from src.shared.domain.valueobject import (
    UUIDValueObject,
    NonEmptyStringValueObject,
    NumericValueObject,
)


class AccountId(UUIDValueObject):
    pass


class AccountName(NonEmptyStringValueObject):
    pass


class AccountIban(NonEmptyStringValueObject):
    pass


class AccountHash(NonEmptyStringValueObject):
    pass


class AccountAmount(NumericValueObject):
    pass


class AccountType(NonEmptyStringValueObject):
    pass


@dataclass
class Account(AggregateRoot):
    id: AccountId
    name: AccountName
    iban: AccountIban
    hash: AccountHash
    amount: AccountAmount
    type: AccountType

    @classmethod
    def create(
        cls,
        name: AccountName,
        iban: AccountIban,
        hash: AccountHash,
        type: AccountType,
        amount: AccountAmount,
    ):
        account = cls(
            id=AccountId.rand(),
            name=name,
            iban=iban,
            hash=hash,
            type=type,
            amount=amount,
        )
        account.record(
            AccountCreated.register({"account_id": str(account.id)})
        )
        return account

    def __hash__(self):
        return hash(self.id)
