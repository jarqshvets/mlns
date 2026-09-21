from src.main.api.db.models.account_table import Account
from sqlalchemy.orm import Session

class AccountCrudDb:
    @staticmethod
    def get_account_by_id(db: Session, account_id: int) -> Account | None:
        return db.query(Account).filter_by(id=account_id).first()

    @staticmethod
    def delete_account_by_id(db: Session, account_id: int) -> None:
        account = db.query(Account).filter_by(id=account_id).first()
        if account:
            db.delete(account) ### удалили внутри сессии
            db.commit() ### сохранили изменения в БД

    @staticmethod
    def get_account_balance(db: Session, account_id: int):
        account = db.query(Account).filter_by(id=account_id).first()
        return account.balance

    @staticmethod
    def get_balance_by_account_id(db: Session, account_id: int) -> float | None:
        account = db.query(Account).filter_by(account_id=account_id).first()
        return account.balance if account else None