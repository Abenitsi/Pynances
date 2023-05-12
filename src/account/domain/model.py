from dataclasses import dataclass

from src.shared.domain.aggregate_root import AggregateRoot
from src.shared.domain.valueobject import (
    UUIDValueObject,
    NonEmptyStringValueObject,
)


class AccountId(UUIDValueObject):
    pass


class AccountName(NonEmptyStringValueObject):
    pass


class AccountIban(NonEmptyStringValueObject):
    pass


class AccountHash(NonEmptyStringValueObject):
    pass


class AccountAmount:
    pass


class AccountType:
    pass


@dataclass
class Account(AggregateRoot):
    id: AccountId
    name: AccountName
    iban: AccountIban
    hash: AccountHash
    amount: AccountAmount
    type: AccountType
