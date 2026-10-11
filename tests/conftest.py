import json
import pytest
from app.schemas.restaurant import RestaurantCreate, Location
from app.services.restaurant_service import RestaurantService
from app.repositories.restaurant_repository import RestaurantRepository
from app.services.menu_service import MenuService
from app.repositories.menu_repository import MenuRepository

@pytest.fixture
def client():
    """Returns a test client for the FastAPI app."""
    from fastapi.testclient import TestClient
    from app.main import app
    return TestClient(app)

@pytest.fixture
def valid_restaurant_payload():
    """Returns valid raw restaurant data for testing."""
    return {
        "name": "Test Restaurant",
        "address": "123 Test St",
        "postalcode": "A1B2C3",
        "phone": "123-456-7890",
        "location": {
            "city": "Test City",
            "province": "Test Province"
        }
    }

@pytest.fixture
def valid_restaurant_create(valid_restaurant_payload):
    """Returns a valid RestaurantCreate object for testing."""
    return RestaurantCreate(**valid_restaurant_payload)

@pytest.fixture
def restaurants_json(tmp_path):
    """Creates a temporary JSON file with restaurant data for testing."""
    data = [
        {
            "id": 1,
            "name": "Test Restaurant 1",
            "address": "123 Test St",
            "postalcode": "A1B2C3",
            "phone": "123-456-7890",
            "rating": "4.9",
            "location": {
                "city": "Test City",
                "province": "Test Province"
            }
        },
        {
            "id": 2,
            "name": "Test Restaurant 2",
            "address": "456 Test Ave",
            "postalcode": "D4E5F6",
            "phone": "987-654-3210",
            "rating": "3.3",
            "location": {
                "city": "Another City",
                "province": "Another Province"
            }
        }
    ]
    file_path = tmp_path / "restaurants.json"
    with open(file_path, 'w') as f:
        json.dump(data, f)
    return str(file_path)

@pytest.fixture
def restaurant_repository(restaurants_json):
    """Returns a RestaurantRepository instance using the temporary JSON file."""
    return RestaurantRepository(file_path=restaurants_json)

@pytest.fixture
def restaurant_service(restaurant_repository):
    """Returns a RestaurantService instance using the provided repository."""
    service = RestaurantService()
    service.repository = restaurant_repository  # Inject the test repository
    return service

@pytest.fixture
def menus_json(tmp_path):
    """Creates a temporary JSON file with menu data for testing."""
    data = [
        {
            "id": 1,
            "restaurant_id": 1,
            "category": "Appetizer",
            "name": "Test Soup",
            "description": "A test soup",
            "price": 5.99
        },
        {
            "id": 2,
            "restaurant_id": 1,
            "category": "Main",
            "name": "Test Pasta",
            "description": "A test pasta",
            "price": 12.50
        },
        {
            "id": 3,
            "restaurant_id": 2,
            "category": "Main",
            "name": "Test Steak",
            "description": "A test steak",
            "price": 18.75
        }
    ]
    file_path = tmp_path / "menus.json"
    with open(file_path, 'w') as f:
        json.dump(data, f)
    return str(file_path)

@pytest.fixture
def menu_service(menus_json):
    """Returns a MenuService instance using the temporary JSON file."""
    service = MenuService()
    service.repository = MenuRepository(file_path=menus_json)  # Inject the test repository
    return service

