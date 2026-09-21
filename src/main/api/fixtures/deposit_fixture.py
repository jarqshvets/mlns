import pytest
from dataclasses import dataclass

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest


@dataclass
class UserWithAccount:
    user: CreateUserRequest
    account_id: int

@pytest.fixture
def user_with_account(
        api_manager: ApiManager,
        create_user_request: CreateUserRequest
) -> UserWithAccount:
    account_response = api_manager.user_steps.create_account(create_user_request)
    return UserWithAccount(
        user=create_user_request,
        account_id=account_response.id)