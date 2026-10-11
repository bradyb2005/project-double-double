from unittest.mock import patch
import pytest 

@pytest.fixture(autouse=True)
def override_router_service(menu_service):
    """Forces the router to use the temporary test file instead of data/restaurants.json"""
    with patch("app.api.routes.menu.service", menu_service):
        yield
        
def test_get_menu_by_restaurant_success(client):
    response = client.get('/restaurants/1/menu')
    assert response.status_code == 200
    assert response.json()[0]['restaurant_id'] == 1
    assert response.json()[1]['restaurant_id'] == 1
    assert len(response.json()) == 2
    assert response.json()[0]['id'] == 1
    
def test_get_menu_by_restaurant_error_404(client):
    response = client.get('/restaurants/99999/menu') 
    assert response.json()['detail'] == "Restaurants menu is empty"
    assert response.status_code == 404
    
def test_get_menu_by_restaurant_details_error_422(client):
    response = client.get('/restaurants/abs/menu')
    assert response.status_code == 422