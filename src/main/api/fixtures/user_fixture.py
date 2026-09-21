import pytest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_credit_user_request(api_manager):
    generated_user = RandomModelGenerator.generate(CreateUserRequest)
    credit_user_request = CreateUserRequest(
        username=generated_user.username,
        password=generated_user.password,
        role="ROLE_CREDIT_SECRET",
    )
    api_manager.admin_steps.create_user(credit_user_request)
    return credit_user_request
