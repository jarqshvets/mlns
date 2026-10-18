import pytest
from sqlalchemy.orm import Session
from src.main.api.test_data.account_test_data import DEPOSIT_VALID_AMOUNT, DEPOSIT_INVALID_BELOW_MIN_AMOUNT
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.deposit_fixture import UserWithAccount
from src.main.api.models.deposit_account_request import DepositAccountRequest


@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account_valid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            user_with_account: UserWithAccount
    ):
        deposit_account_request = DepositAccountRequest(
            accountId=user_with_account.account_id,
            amount=DEPOSIT_VALID_AMOUNT
        )
        response = api_manager.user_steps.deposit_account(user_with_account.user, deposit_account_request)
        assert response.balance == DEPOSIT_VALID_AMOUNT, 'Сумма на балансе не совпадает с суммой пополнения'

        account_from_db = AccountCrudDb.get_account_by_id(db_session, response.id)
        assert account_from_db.balance == response.balance, 'Баланс аккаунта в БД не пополнен'




    def test_deposit_account_invalid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            user_with_account: UserWithAccount
    ):
        deposit_account_request = DepositAccountRequest(
            accountId=user_with_account.account_id,
            amount=DEPOSIT_INVALID_BELOW_MIN_AMOUNT
        )
        api_manager.user_steps.deposit_account_invalid(user_with_account.user, deposit_account_request)
        account_from_db = AccountCrudDb.get_account_by_id(db_session, user_with_account.account_id)
        assert account_from_db.balance == 0, 'Баланс аккаунта в БД пополнен на сумму, меньше минимальной'