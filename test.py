import string
import random

from src import CoreConfig
from src.account.application.unit_of_work import AccountUoW
from src.account.domain.model import AccountId
from src.account.infrastructure.repository import SQLAlchemyAccountRepository

from src.sdk import SDK
from src.shared.dependency_container import DependencyContainer
from src.shared.domain.domain_event import DomainEventId
from src.shared.infrastructure.repository import SqlAlchemyEventRepository

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
    hash="".join(random.choice(string.ascii_lowercase) for i in range(32)),
)

repo = sdk._SDK__container.get(SqlAlchemyEventRepository)
event = repo.get(DomainEventId("290fd055-9c7a-4d62-abb7-d01b54d9a436"))
print(event)
