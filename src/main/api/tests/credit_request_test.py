import pytest
from sqlalchemy.orm import Session
from src.main.api.test_data.account_test_data import CREDIT_VALID_AMOUNT, CREDIT_INVALID_BELOW_MIN_AMOUNT, CREDIT_VALID_TERM
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.user_credit_role_fixture import UserWithCreditRoleAccount
from src.main.api.models.credit_request_request import CreditRequestRequest

@pytest.mark.api
class TestCreditRequest:
    def test_credit_request_valid(self, db_session: Session, api_manager: ApiManager, user_credit_role_with_account: UserWithCreditRoleAccount):

        credit_request_request = CreditRequestRequest(
            accountId=user_credit_role_with_account.account_id,
            amount=CREDIT_VALID_AMOUNT,
            termMonths=CREDIT_VALID_TERM
        )
        response = api_manager.user_steps.credit_request(user_credit_role_with_account.user, credit_request_request)
        assert credit_request_request.amount == response.amount, 'Сумма кредита не совпадает с запрошенной'
        assert credit_request_request.termMonths == response.termMonths, 'Срок кредита не совпадает с запрошенным'

        credit_from_db = CreditCrudDb.get_credit_by_account_id(db_session, user_credit_role_with_account.account_id)
        assert credit_from_db.id == response.creditId, 'айди кредита нет в БД'

    def test_credit_request_invalid(self, db_session: Session, api_manager: ApiManager, user_credit_role_with_account: UserWithCreditRoleAccount):

        credit_request_request = CreditRequestRequest(
            accountId=user_credit_role_with_account.account_id,
            amount=CREDIT_INVALID_BELOW_MIN_AMOUNT,
            termMonths=CREDIT_VALID_TERM
        )
        api_manager.user_steps.credit_request_invalid(user_credit_role_with_account.user, credit_request_request)
        credit_from_db = CreditCrudDb.get_credit_by_account_id(db_session, user_credit_role_with_account.account_id)
        assert credit_from_db is None, 'Кредит с некорректной ролью юзера создался'