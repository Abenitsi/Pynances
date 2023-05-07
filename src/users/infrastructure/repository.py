from src.shared.infrastructure.repository import SqlAlchemyConnection
from src.users.domain.repository import UserRepository
from src.users.domain.user import UserId, User


class SqlAlchemyUserRepository(UserRepository):
    connection: SqlAlchemyConnection

    def by_id(self, user_id: UserId) -> User:
        users = self.connection.read(User, User.id == user_id)
        user: User = users[0]
        return user

    def save(self, user: User) -> None:
        self.connection.write(user)
