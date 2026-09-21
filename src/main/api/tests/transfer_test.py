import pytest
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.transfer_fixture import TransferReadyUser
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.test_data.account_test_data import TRANSFER_VALID_AMOUNT, TRANSFER_INVALID_BELOW_MIN_AMOUNT


@pytest.mark.api
class TestTransfer:
    def test_transfer_valid(self, db_session: Session, api_manager: ApiManager, user_with_two_accounts_and_balance: TransferReadyUser):
        transfer_request = TransferRequest(
            fromAccountId=user_with_two_accounts_and_balance.from_account_id,
            toAccountId=user_with_two_accounts_and_balance.to_account_id,
            amount=TRANSFER_VALID_AMOUNT
        )
        response = api_manager.user_steps.transfer(user_with_two_accounts_and_balance.user, transfer_request)
        assert transfer_request.fromAccountId == response.fromAccountId, 'ID счета отправителя не совпадает с фактическим'
        assert transfer_request.toAccountId == response.toAccountId, 'ID счета получателя не совпадает с фактическим'

        to_account_transfer = AccountCrudDb.get_account_by_id(db_session, response.toAccountId)
        assert to_account_transfer.balance == TRANSFER_VALID_AMOUNT, 'Балансы счетов не изменились, перевод не зафиксирован в БД'



    def test_transfer_invalid(self, db_session: Session, api_manager: ApiManager, user_with_two_accounts_and_balance: TransferReadyUser):
        transfer_request = TransferRequest(
            fromAccountId=user_with_two_accounts_and_balance.from_account_id,
            toAccountId=user_with_two_accounts_and_balance.to_account_id,
            amount=TRANSFER_INVALID_BELOW_MIN_AMOUNT
        )
        api_manager.user_steps.transfer_invalid(user_with_two_accounts_and_balance.user, transfer_request)

        account_from_db = AccountCrudDb.get_account_by_id(db_session, user_with_two_accounts_and_balance.to_account_id)
        assert account_from_db.balance == 0, 'Баланс принимающего счёта не изменился'
