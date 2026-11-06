import pytest
from app.schemas.user import LoginRequest


class TestLogin:
    def test_login_returns_access_token(self, login_service):
        response = login_service.login(
            LoginRequest(
                email="john.doe@example.com",
                password="SecurePassword123!",
            )
        )

        assert response.access_token
        assert response.token_type == "bearer"

    def test_login_rejects_missing_account(self, login_service):
        with pytest.raises(ValueError, match="Invalid email or password"):
            login_service.login(
                LoginRequest(
                    email="missing@example.com",
                    password="SecurePassword123!",
                )
            )

    def test_login_rejects_incorrect_password(self, login_service):
        with pytest.raises(ValueError, match="Invalid email or password"):
            login_service.login(
                LoginRequest(
                    email="john.doe@example.com",
                    password="WrongPassword123!",
                )
            )

    def test_login_rejects_inactive_user(self, login_user, login_service):
        login_user["is_active"] = False

        with pytest.raises(ValueError, match="Invalid email or password"):
            login_service.login(
                LoginRequest(
                    email="john.doe@example.com",
                    password="SecurePassword123!",
                )
            )
