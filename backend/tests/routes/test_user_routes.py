import pytest
from app.main import app
from app.services.user_service import UserService
from fastapi import status


@pytest.fixture(autouse=True)
def override_dependency(user_service):
    app.dependency_overrides[UserService] = lambda: user_service
    yield
    app.dependency_overrides.clear()

class TestUserGet:
    def test_get_users_requires_admin_role(self, client, auth_headers):
        response = client.get("/users", headers=auth_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_user_details_requires_authentication(self, client):
        response = client.get("/users/1")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_fetch_user_details_success(self, client, auth_headers):
        response = client.get("/users/1", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == 1

    def test_fetch_user_details_forbidden_for_another_user(self, client, auth_headers):
        response = client.get("/users/99999", headers=auth_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_fetch_user_details_error_422(self, client, auth_headers):
        response = client.get("/users/abc", headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_fetch_user_details_rejects_invalid_token(self, client):
        response = client.get(
            "/users/1",
            headers={"Authorization": "Bearer invalid"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_fetch_user_details_rejects_inactive_user(
        self,
        client,
        auth_headers,
        user_service,
    ):
        user_service.deactivate_user(1)

        response = client.get("/users/1", headers=auth_headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_users_rejects_restaurant_role(
        self,
        client,
        auth_headers,
        user_repository,
    ):
        user_repository.update_user(1, {"role": "restaurant"})

        response = client.get("/users", headers=auth_headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_users_allows_admin_role(
        self,
        client,
        auth_headers,
        user_repository,
    ):
        user_repository.update_user(1, {"role": "admin"})

        response = client.get("/users", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

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
            headers={"Authorization": "Bearer invalid"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_user_with_authentication(self, client, auth_headers):
        response = client.put(
            "/users/1",
            json={"firstname": "Updated"},
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["firstname"] == "Updated"

    def test_update_user_forbidden_for_another_user(self, client, auth_headers):
        response = client.put(
            "/users/99999",
            json={"firstname": "Updated"},
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

class TestUserDeactivate:
    def test_deactivate_user_requires_authentication(self, client):
        response = client.put("/users/1/deactivate")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_deactivate_user_success(self, client, auth_headers):
        response = client.put("/users/1/deactivate", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["is_active"] is False

    def test_deactivate_user_forbidden_for_another_user(self, client, auth_headers):
        response = client.put("/users/99999/deactivate", headers=auth_headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN