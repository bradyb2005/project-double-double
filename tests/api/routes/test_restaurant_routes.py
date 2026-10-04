from unittest.mock import patch
import pytest

@pytest.fixture(autouse=True)
def override_router_service(restaurant_service):
    """Forces the router to use the temporary test file instead of data/restaurants.json"""
    with patch("app.api.routes.restaurants.service", restaurant_service):
        yield

def test_get_restaurants(client):
    response = client.get("/restaurants")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_restaurant_success(client, valid_restaurant_payload):
    response = client.post("/restaurants", json=valid_restaurant_payload)
    assert response.status_code == 201
    assert response.json()["name"] == valid_restaurant_payload["name"]

def test_create_restaurant_error_400(client, valid_restaurant_payload):
    valid_restaurant_payload["phone"] = "invalid-phone"
    response = client.post("/restaurants", json=valid_restaurant_payload)
    assert response.status_code == 400

def test_fetch_restaurant_details_success(client):
    response = client.get("/restaurants/1")
    assert response.status_code == 200

def test_fetch_restaurant_details_error_404(client):
    response = client.get("/restaurants/99999")
    assert response.status_code == 404
    
def test_fetch_restaurant_details_error_422(client):
    response = client.get("/restaurants/abc")
    assert response.status_code == 422