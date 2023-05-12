from src.account.domain.model import Account, AccountId
from src.account.domain.repository import AccountRepository
from src.shared.infrastructure.connection import SQLAlchemyConnection


class SQLAlchemyAccountRepository(AccountRepository):
    connection: SQLAlchemyConnection

    def save(self, account: Account):
        pass

    def get(self, account_id: AccountId):
        pass
