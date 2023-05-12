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


class Create(UseCase):
    def __call__(self) -> None:
        account = Account(
            id=AccountId.rand(),
            name=AccountName("Cuenta"),
            iban=AccountIban("Iban"),
            hash=AccountHash("hash"),
            type=AccountType(),
            amount=AccountAmount(),
        )

        print(account)
