import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.fixtures.credit_fixture import UserWithCreditAccount
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.test_data.account_test_data import CREDIT_VALID_AMOUNT


@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay_valid(self,db_session: Session, api_manager: ApiManager, user_with_credit_account: UserWithCreditAccount):

        credit_repay_request = CreditRepayRequest(creditId=user_with_credit_account.credit_id, accountId=user_with_credit_account.account_id, amount=user_with_credit_account.amount)
        response = api_manager.user_steps.credit_repay(user_with_credit_account.user, credit_repay_request)
        assert credit_repay_request.creditId == response.creditId, 'id кредита в запросе и ответе не совпадают'

        credit_from_db = CreditCrudDb.get_credit_by_id(db_session, user_with_credit_account.credit_id)
        assert credit_from_db.balance == 0, 'Сумма кредита не равна 0, погашение кредита не прошло в БД'


    def test_credit_repay_invalid(self, db_session: Session, api_manager: ApiManager, user_with_credit_account: UserWithCreditAccount):

        credit_repay_request = CreditRepayRequest(creditId=user_with_credit_account.credit_id, accountId=user_with_credit_account.account_id, amount=CREDIT_VALID_AMOUNT + 1)
        api_manager.user_steps.credit_repay_invalid(user_with_credit_account.user, credit_repay_request)

        credit_from_db = CreditCrudDb.get_credit_by_id(db_session, user_with_credit_account.credit_id)
        assert credit_from_db.balance == -CREDIT_VALID_AMOUNT, 'Сумма кредита не изменилась в БД'