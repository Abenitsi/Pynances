from src import CoreConfig

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

account = sdk.account.create(
    name="My Account",
    iban="My Iban",
    amount=0,
    type="savings",
    hash="my hash 3",
)
