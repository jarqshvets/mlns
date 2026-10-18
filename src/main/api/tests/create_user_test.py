import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)],
    )
    def test_create_user_valid(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            db_session: Session
    ):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username, 'Имя пользователя в запросе и ответе не совпадают'
        assert create_user_request.role == response.role, 'Роль пользователя не соответствует заданной'

        user_from_db = User.get_user_by_username(db_session, response.username)
        assert user_from_db.username == create_user_request.username, 'Созданного пользователя нет в БД'

    @pytest.mark.parametrize(
        "username, password",
        [
            ("абв", "Pas!sw0rd"),
            ("Ia", "Pas!sw0rd"),
            ("Iaroslav12345678", "Pas!sw0rd"),
            ("@Iar", "Pas!sw0rd"),
            ("Iar1", "Пas!sw0rd"),
            ("Iar2", "Pas!sw0"),
            ("Iar3", "pas!sw0rd"),
            ("Iar4", "PAS!SW0RD"),
            ("Iar5", "Passw0rd"),
            ("Iar6", "Pas!swOrd")
        ]
    )
    def test_create_user_invalid(self, db_session: Session,username: str, password: str, api_manager: ApiManager):

        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_invalid_user(create_user_request)
        user_from_bd = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_bd is None, 'Пользователь создан, ошибка'