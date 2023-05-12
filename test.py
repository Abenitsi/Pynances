from src import CoreConfig
from src.account.domain.model import (
    Account,
    AccountId,
    AccountName,
    AccountIban,
    AccountType,
    AccountAmount,
    AccountHash,
)

from src.sdk import SDK

sdk = SDK(
    CoreConfig(
        db_driver="postgresql",
        db_user="postgres",
        db_password="postgrespassword",
        db_host="127.0.0.1:5432",
        db_name="pynances",
    )
)

account = sdk.account.create()
print(account)
