import sqlalchemy
from sqlalchemy import Column, Table
from sqlalchemy.orm import registry

from src.shared.class_locator import ClassLocator
from src.shared.domain.domain_event import (
    DomainEvent,
    DomainEventOccurredAt,
    DomainEventName,
    DomainEventData,
    DomainEventId,
)
from src.shared.infrastructure.repository import type_decorator_factory

"""
    MAPPING
"""

mapper_registry = registry()

try:
    account_table = Table(
        "domain_events",
        mapper_registry.metadata,
        Column(
            "id", type_decorator_factory(DomainEventId, True), primary_key=True
        ),
        Column(
            "occurred_at", type_decorator_factory(DomainEventOccurredAt, False)
        ),
        Column("name", type_decorator_factory(DomainEventName, True)),
        Column("data", type_decorator_factory(DomainEventData, False)),
    )

    mapper_registry.map_imperatively(
        DomainEvent,
        account_table,
        polymorphic_on=account_table.c.name,
        polymorphic_identity=DomainEvent.__module__
        + "."
        + DomainEvent.__name__,
    )

    event_modules = ClassLocator.locate(
        path="src",
        class_name=DomainEvent,
        skip_modules=[
            ".DS_Store",
            "__pycache__",
            "sdk",
            "infrastructure",
            "application",
            "model.py",
        ],
    )

    for module in event_modules:
        for event in module["classes"]:
            mapper_registry.map_imperatively(
                event,
                inherits=DomainEvent,
                polymorphic_identity=str(module["module"])
                + "."
                + event.__name__,
            )

except sqlalchemy.exc.ArgumentError:
    pass
