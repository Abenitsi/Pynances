from typing import Self

from src.shared.domain.aggregate_root import AggregateRoot
from src.shared.domain.domain_event import DomainEvent, DomainEventId
from src.shared.domain.valueobject import (
    EmailValueObject,
    NonEmptyStringValueObject,
    UUIDValueObject,
)


class UserId(UUIDValueObject):
    pass


class UserEmail(EmailValueObject):
    pass


class UserName(NonEmptyStringValueObject):
    pass


class UserSurname(NonEmptyStringValueObject):
    pass


class UserCreated(DomainEvent):
    pass


class User(AggregateRoot):
    id: UserId
    name: UserName
    email: UserEmail

    def __init__(self, id: UserId, name: UserName, email: UserEmail) -> None:
        self.id = id
        self.name = name
        self.email = email

    @classmethod
    def create(
        cls,
        user_id: str,
        name: str,
        email: str,
    ) -> Self:
        user = cls(
            id=UserId(user_id),
            name=UserName(name),
            email=UserEmail(email),
        )
        user.record(UserCreated(id=DomainEventId.rand(), data="aaa"))
        return user

    def __str__(self) -> str:
        return (
            "Id: "
            + self.id
            + "\n"
            + "Name: "
            + self.name
            + "\n"
            + "Email: "
            + self.email
        )
