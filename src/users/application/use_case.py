from src.users.domain.repository import UserRepository
from src.shared.application.use_case import UseCase
from src.users.domain.user import User, UserId


class CreateUser(UseCase):
    def __init__(self, repository: UserRepository):
        self.repository: UserRepository = repository

    def __call__(
        self,
        name: str,
        email: str,
    ) -> User:
        """
        print(UserId.rand())
        user = User.create(
            UserId.rand().value,
            name,
            email,
        )
        self.repository.save(user)
        """
        user_id = UserId("f3a5303a-a75d-45e7-98b4-8639771e6daf")

        user = self.repository.by_id(user_id)

        return user
