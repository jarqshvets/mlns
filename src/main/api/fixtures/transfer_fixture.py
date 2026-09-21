from dataclasses import dataclass
import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest



@dataclass
class TransferReadyUser:
    user: CreateUserRequest
    from_account_id: int
    to_account_id: int
    initial_balance: float


@pytest.fixture
def user_with_two_accounts_and_balance(
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
) -> TransferReadyUser:
    initial_balance = 1000
    source_account = api_manager.user_steps.create_account(create_user_request)
    deposit_request = DepositAccountRequest(
        accountId=source_account.id,
        amount=initial_balance
    )
    api_manager.user_steps.deposit_account(
        create_user_request,
        deposit_request
    )
    target_account = api_manager.user_steps.create_account(create_user_request)
    return TransferReadyUser(
        user=create_user_request,
        from_account_id=source_account.id,
        to_account_id=target_account.id,
        initial_balance=initial_balance
    )