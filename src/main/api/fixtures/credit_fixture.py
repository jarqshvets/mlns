from src.main.api.fixtures.api_fixture import ApiManager
from dataclasses import dataclass
import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.test_data.account_test_data import CREDIT_VALID_AMOUNT, CREDIT_VALID_TERM


@dataclass
class UserWithCreditAccount:
    user: CreateUserRequest
    credit_id: int
    account_id: int
    amount: int

@pytest.fixture
def user_with_credit_account(
        api_manager: ApiManager,
        create_credit_user_request: CreateUserRequest
) -> UserWithCreditAccount:
    credit_account = api_manager.user_steps.create_account(create_credit_user_request)
    credit_request = CreditRequestRequest(
        accountId=credit_account.id,
        amount=CREDIT_VALID_AMOUNT,
        termMonths=CREDIT_VALID_TERM
    )
    credit_response = api_manager.user_steps.credit_request(
        create_credit_user_request, credit_request)
    return UserWithCreditAccount(
        user=create_credit_user_request,
        credit_id=credit_response.creditId,
        account_id=credit_response.id,
        amount=CREDIT_VALID_AMOUNT
    )
