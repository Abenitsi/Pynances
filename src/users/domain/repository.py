from abc import ABC, abstractmethod
from src.shared.domain.repositories import Repository
from src.users.domain.user import UserId, User


class UserRepository(Repository, ABC):
    @abstractmethod
    def by_id(self, user_id: UserId) -> User:
        pass

    @abstractmethod
    def save(self, user: User) -> None:
        pass
