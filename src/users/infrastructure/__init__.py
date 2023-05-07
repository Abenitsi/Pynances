from src.shared.infrastructure.repository import type_decorator_factory
from sqlalchemy.orm import registry, column_property
from sqlalchemy import Column, Table
from src.users.domain.user import UserId, UserName, UserEmail, User

"""
    MAPPING
"""
mapper_registry = registry()

users_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", type_decorator_factory(UserId, True), primary_key=True),
)

mapper_registry.map_imperatively(
    User,
    users_table,
    properties={
        "name": column_property(
            Column("name", type_decorator_factory(UserName, False))
        ),
        "email": column_property(
            Column("email", type_decorator_factory(UserEmail, False))
        ),
    },
)
"""
@dataclass
class DBUser2:
    user_id: UserId
    user_name: str
mapper_registry.map_imperatively(
    DBUser2, users_table, properties={
        "user_id": Column("id", UserIdDecorator, primary_key=True),
        "user_name": users_table.c.name,
    }
)
"""
