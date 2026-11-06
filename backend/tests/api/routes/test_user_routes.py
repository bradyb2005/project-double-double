import pytest
from app.main import app
from app.services.user_service import UserService


@pytest.fixture(autouse=True)
def override_dependency(user_service):
    app.dependency_overrides[UserService] = lambda: user_service
    yield
    app.dependency_overrides.clear()

class TestUserGet:
    def test_get_users(self, client):
        response = client.get("/users")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_fetch_user_details_success(self, client):
        response = client.get("/users/1")
        assert response.status_code == 200

    def test_fetch_user_details_error_404(self, client):
        response = client.get("/users/99999")
        assert response.status_code == 404

    def test_fetch_user_details_error_422(self, client):
        response = client.get("/users/abc")
        assert response.status_code == 422

class TestUserCreate:
    def test_create_user_success(self, client, valid_user_payload):
        response = client.post("/users", json=valid_user_payload)
        assert response.status_code == 201
        assert response.json()["email"] == valid_user_payload["email"]

    def test_create_user_error_400(self, client, valid_user_payload):
        valid_user_payload["phone"] = "invalid-phone"
        response = client.post("/users", json=valid_user_payload)
        assert response.status_code == 422

class TestUserUpdate:
    def test_update_user_success(self, client):
        response = client.put(
            "/users/1",
            json={"firstname": "Updated", "is_active": False},
        )

        assert response.status_code == 200
        assert response.json()["firstname"] == "Updated"
        assert response.json()["is_active"] is False

    def test_update_user_error_404(self, client):
        response = client.put("/users/99999", json={"firstname": "Updated"})

        assert response.status_code == 404

class TestUserDeactivate:
    def test_deactivate_user_success(self, client):
        response = client.put("/users/1/deactivate")

        assert response.status_code == 200
        assert response.json()["is_active"] is False

    def test_deactivate_user_error_404(self, client):
        response = client.put("/users/99999/deactivate")

        assert response.status_code == 404