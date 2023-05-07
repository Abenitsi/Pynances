from typing import Callable

from src.shared.DependencyContainer import DependencyContainer
from src.shared.domain.domain_event import DomainEventRepository
from src.shared.domain.repositories import Connection
from src.shared.infrastructure.repository import (
    InMemoryEventRepository,
    SqlAlchemyConnection,
)
from src.users.domain.repository import UserRepository
from src.users.infrastructure.repository import SqlAlchemyUserRepository

container = DependencyContainer.get_container()

### Interface bindings ###
container.set(DependencyContainer, container)
container.set(DomainEventRepository, container.get(InMemoryEventRepository))


connection = SqlAlchemyConnection(
    driver="postgresql",
    user="postgres",
    password="postgrespassword",
    host="127.0.0.1:5432",
    db_name="postgres",
)
container.set(Connection, connection)
container.set(UserRepository, container.get(SqlAlchemyUserRepository))
