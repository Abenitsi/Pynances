import string
import random

from src import CoreConfig
from src.account.application.unit_of_work import AccountUoW
from src.account.domain.model import AccountId, AccountType
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
    name="Cuenta Nómina Comuna",
    iban="ES56 1465 0120 38 1742779152",
    amount=0,
    type="regular",
)
