from src.account.domain.model import Account, AccountId
from src.account.domain.repository import AccountRepository
from src.shared.infrastructure.connection import SQLAlchemyConnection


class SQLAlchemyAccountRepository(AccountRepository):
    connection: SQLAlchemyConnection

    def save(self, account: Account) -> None:
        self.connection.write(account)

    def get(self, account_id: AccountId) -> Account:
        accounts = self.connection.read(Account, Account.id == account_id)
        account: Account = accounts[0]
        return account
