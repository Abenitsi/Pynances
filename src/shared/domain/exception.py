class DomainException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class EmptyValue(DomainException):
    def __init__(self) -> None:
        super().__init__("Value cannot be empty")


class InvalidEmailValue(DomainException):
    def __init__(self) -> None:
        super().__init__("Value is not a valid email")


class InvalidIdValue(DomainException):
    def __init__(self) -> None:
        super().__init__("Value is not a valid id")
