import pytest
from app.api.routes.login import get_login_service
from app.main import app
from fastapi import status


@pytest.fixture(autouse=True)
def override_login_dependency(login_service):
    app.dependency_overrides[get_login_service] = lambda: login_service
    yield
    app.dependency_overrides.pop(get_login_service, None)


class TestLoginRoute:
    def test_login_returns_token(self, client):
        response = client.post(
            "/login",
            json={
                "email": "john.doe@example.com",
                "password": "SecurePassword123!",
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["token_type"] == "bearer"
        assert response.json()["access_token"]

    @pytest.mark.parametrize(
        "payload",
        [
            {
                "email": "missing@example.com",
                "password": "SecurePassword123!",
            },
            {
                "email": "john.doe@example.com",
                "password": "WrongPassword123!",
            },
        ],
    )
    def test_login_returns_401_for_invalid_credentials(self, client, payload):
        response = client.post("/login", json=payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Invalid email or password"
        assert response.headers["www-authenticate"] == "Bearer"

    def test_login_returns_422_for_invalid_request(self, client):
        response = client.post(
            "/login",
            json={"email": "not-an-email", "password": "short"},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
