import pytest
from dataclasses import dataclass
from src.main.api.fixtures.api_fixture import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest


@dataclass
class UserWithCreditRoleAccount:
    user: CreateUserRequest
    account_id: int


@pytest.fixture
def user_credit_role_with_account(
        api_manager: ApiManager,
        create_credit_user_request: CreateUserRequest
) -> UserWithCreditRoleAccount:
    account_response = api_manager.user_steps.create_account(create_credit_user_request)
    return UserWithCreditRoleAccount(
        user=create_credit_user_request,
        account_id=account_response.id)