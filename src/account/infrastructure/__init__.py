import sqlalchemy
from sqlalchemy import Column, Table, ForeignKey, Enum
from sqlalchemy.orm import registry, relationship

from src.shared.infrastructure.repository import type_decorator_factory
from src.account.domain.model import (
    Account,
    AccountType,
    AccountHash,
    AccountIban,
    AccountName,
    AccountAmount,
    AccountId,
    MovementId,
    MovementDescription,
    MovementHash,
    MovementConcept,
    MovementAmount,
    MovementCategory,
    MovementDate,
    Movement,
)

"""
    MAPPING
"""

mapper_registry = registry()

try:
    account_table = Table(
        "accounts",
        mapper_registry.metadata,
        Column(
            "id", type_decorator_factory(AccountId, True), primary_key=True
        ),
        Column("name", type_decorator_factory(AccountName, False)),
        Column("hash", type_decorator_factory(AccountHash, False)),
        Column("iban", type_decorator_factory(AccountIban, False)),
        Column(
            "type",
            Enum(
                AccountType, values_callable=lambda obj: [str(e) for e in obj]
            ),
        ),
        Column("amount", type_decorator_factory(AccountAmount, False)),
    )

    movements_table = Table(
        "movements",
        mapper_registry.metadata,
        Column(
            "id", type_decorator_factory(MovementId, True), primary_key=True
        ),
        Column("hash", type_decorator_factory(MovementHash, False)),
        Column("concept", type_decorator_factory(MovementConcept, False)),
        Column(
            "description", type_decorator_factory(MovementDescription, False)
        ),
        Column("amount", type_decorator_factory(MovementAmount, False)),
        Column("category", type_decorator_factory(MovementCategory, False)),
        Column("date", type_decorator_factory(MovementDate, False)),
        Column(
            "account_id",
            type_decorator_factory(AccountId, False),
            ForeignKey("accounts.id"),
        ),
    )

    mapper_registry.map_imperatively(Movement, movements_table)

    mapper_registry.map_imperatively(
        Account,
        account_table,
        properties={
            "movements": relationship(
                Movement,
                primaryjoin=account_table.c.id == movements_table.c.account_id,
            )
        },
    )
except sqlalchemy.exc.ArgumentError:
    pass
