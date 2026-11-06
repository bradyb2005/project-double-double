import pytest
from app.main import app
from app.services.user_service import UserService


@pytest.fixture(autouse=True)
def override_dependency(user_service):
    app.dependency_overrides[UserService] = lambda: user_service
    yield
    app.dependency_overrides.clear()

def test_get_users(client):
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_user_success(client, valid_user_payload):
    response = client.post("/users", json=valid_user_payload)
    assert response.status_code == 201
    assert response.json()["email"] == valid_user_payload["email"]

def test_create_user_error_400(client, valid_user_payload):
    valid_user_payload["phone"] = "invalid-phone"
    response = client.post("/users", json=valid_user_payload)
    assert response.status_code == 422

def test_fetch_user_details_success(client):
    response = client.get("/users/1")
    assert response.status_code == 200

def test_fetch_user_details_error_404(client):
    response = client.get("/users/99999")
    assert response.status_code == 404

def test_fetch_user_details_error_422(client):
    response = client.get("/users/abc")
    assert response.status_code == 422