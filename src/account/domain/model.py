import hashlib
from dataclasses import dataclass
from enum import StrEnum
from typing import Self, Any

from src.account.domain.events import AccountCreated
from src.shared.domain.aggregate_root import AggregateRoot
from src.shared.domain.valueobject import (
    UUIDValueObject,
    NonEmptyStringValueObject,
    NumericValueObject,
    StringValueObject,
    TimestampValueObject,
)


class MovementId(UUIDValueObject):
    pass


class MovementConcept(NonEmptyStringValueObject):
    pass


class MovementDescription(StringValueObject):
    pass


class MovementAmount(NumericValueObject):
    pass


class MovementDate(TimestampValueObject):
    pass


class MovementCategory(str):
    pass


class MovementHash(NonEmptyStringValueObject):
    pass


@dataclass
class Movement:
    id: MovementId
    concept: MovementConcept
    description: MovementDescription
    category: MovementCategory
    amount: MovementAmount
    date: MovementDate
    hash: MovementHash


class AccountId(UUIDValueObject):
    pass


class AccountName(NonEmptyStringValueObject):
    pass


class AccountIban(NonEmptyStringValueObject):
    pass


class AccountHash(NonEmptyStringValueObject):
    @classmethod
    def from_str(cls, hash_str: str) -> Self:
        return AccountHash(
            hashlib.sha256((str(hash_str).encode("utf-8"))).hexdigest()
        )


class AccountAmount(NumericValueObject):
    pass


class AccountType(StrEnum):
    REGULAR = "regular"
    SAVING = "saving"


@dataclass
class Account(AggregateRoot):
    id: AccountId
    name: AccountName
    iban: AccountIban
    hash: AccountHash
    amount: AccountAmount
    type: AccountType
    movements: list[Movement]

    @classmethod
    def create(
        cls,
        name: AccountName,
        iban: AccountIban,
        type: AccountType,
        amount: AccountAmount,
    ):
        account = cls(
            id=AccountId.rand(),
            name=name,
            iban=iban,
            hash=AccountHash.from_str(str(iban)),
            type=type,
            amount=amount,
            movements=list(),
        )
        account.record(
            AccountCreated.register({"account_id": str(account.id)})
        )
        return account

    def __hash__(self):
        return hash(self.id)
