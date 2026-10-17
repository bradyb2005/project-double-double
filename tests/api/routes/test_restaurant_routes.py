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

def test_get_menu_by_restaurant_success(client):
    response = client.get("/restaurants/1/menu")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["id"] == 1
    assert response.json()[0]["name"] == "Test Soup"
    assert response.json()[0]["description"] == "A test soup"
    assert response.json()[0]["availability"] is True

def test_get_menu_by_restaurant_empty_menu(client):
    response = client.get("/restaurants/2/menu")
    assert response.status_code == 200
    assert response.json() == []

def test_get_menu_by_restaurant_error_404(client):
    response = client.get("/restaurants/99999/menu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Restaurant not found"

def test_get_menu_by_restaurant_error_422(client):
    response = client.get("/restaurants/abc/menu")
    assert response.status_code == 422

def test_fetch_restaurant_names_success(client):
    response = client.get("/restaurants/names")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "Test Restaurant 1" in response.json()
    assert "Test Restaurant 2" in response.json()

def test_get_restaurants_search_query(client):
    response = client.get("/restaurants?search=mexican")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Restaurant 2"

def test_get_restaurants_filter_by_cuisine(client):
    response = client.get("/restaurants?cuisine=Italian")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(r["cuisine"] == "Italian" for r in data)

def test_get_restaurants_filter_by_city(client):
    response = client.get("/restaurants?city=Test City")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Restaurant 1"

def test_get_restaurants_filter_by_province(client):
    response = client.get("/restaurants?province=Another Province")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(r["location"]["province"] == "Another Province" for r in data)

def test_get_restaurants_filter_by_rating(client):
    response = client.get("/restaurants?rating=4.0")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(r["rating"] >= 4.0 for r in data)

def test_get_restaurants_multi_query(client):
    response = client.get("/restaurants?cuisine=Italian&rating=4.0")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Restaurant 1"

def test_get_restaurants_no_match(client):
    response = client.get("/restaurants?search=nonexistent")
    assert response.status_code == 200
    assert response.json() == []