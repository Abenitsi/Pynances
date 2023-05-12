from sqlalchemy import Column, Table
from sqlalchemy.orm import registry

from src.shared.infrastructure.repository import type_decorator_factory
from src.account.domain.model import (
    Account,
    AccountType,
    AccountHash,
    AccountIban,
    AccountName,
    AccountAmount,
    AccountId,
)

"""
    MAPPING
"""
mapper_registry = registry()

account_table = Table(
    "accounts",
    mapper_registry.metadata,
    Column("id", type_decorator_factory(AccountId, True), primary_key=True),
    Column("name", type_decorator_factory(AccountName, False)),
    Column("hash", type_decorator_factory(AccountHash, False)),
    Column("iban", type_decorator_factory(AccountIban, False)),
    Column("type", type_decorator_factory(AccountName, False)),
    Column("amount", type_decorator_factory(AccountAmount, False)),
)

mapper_registry.map_imperatively(Account, account_table)
