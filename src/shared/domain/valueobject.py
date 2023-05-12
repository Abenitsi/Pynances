from abc import ABC
from re import compile, fullmatch
from typing import Any, Self
from uuid import UUID, uuid4

import ulid

from src.shared.domain.exception import (
    EmptyValue,
    InvalidEmailValue,
    InvalidIdValue,
)


class ValidatedValueObject(ABC):
    def __new__(cls, *args: Any, **kwargs: Any) -> "ValidatedValueObject":
        instance = super().__new__(cls, *args, **kwargs)
        cls._validate(args[0])
        return instance

    @staticmethod
    def _validate(value: Any) -> None:
        """Raise exception if validation is not successful"""


class StringValueObject(ValidatedValueObject, str):
    def _validate(value: Any) -> None:
        if not isinstance(value, str):
            raise TypeError()


class NonEmptyStringValueObject(StringValueObject):
    @staticmethod
    def _validate(value: Any) -> None:
        super(NonEmptyStringValueObject, NonEmptyStringValueObject)._validate(
            value
        )
        if len(value) == 0:
            raise EmptyValue()


class UUIDValueObject(NonEmptyStringValueObject):
    @classmethod
    def rand(cls) -> Self:
        return cls(str(uuid4()))

    @staticmethod
    def _validate(value: Any) -> None:
        super(UUIDValueObject, UUIDValueObject)._validate(value)
        try:
            UUID(value)
        except ValueError:
            raise InvalidIdValue()


class ULIDValueObject(NonEmptyStringValueObject):
    @classmethod
    def rand(cls) -> Self:
        return cls(str(ulid.new()))

    @staticmethod
    def _validate(value: Any) -> None:
        super(ULIDValueObject, ULIDValueObject)._validate(value)
        try:
            ulid.from_str(value)
        except ValueError:
            raise InvalidIdValue()


class EmailValueObject(NonEmptyStringValueObject):
    @staticmethod
    def _validate(value: Any) -> None:
        super(EmailValueObject, EmailValueObject)._validate(value)
        regex = compile(
            r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])"
        )
        if not fullmatch(regex, value):
            raise InvalidEmailValue()


class NumericValueObject(ValidatedValueObject, float):
    def _validate(value: Any) -> None:
        if not isinstance(value, float) and not isinstance(value, int):
            raise TypeError()
