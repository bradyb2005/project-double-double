import json

import pytest
from app.main import app
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.menu_item import ItemCreate
from app.schemas.restaurant import RestaurantCreate, RestaurantFilter
from app.services.restaurant_service import RestaurantService


@pytest.fixture(autouse=True)
def override_dependency(restaurant_service):
    """Overrides the FastAPI service dependency to use the test repository fixture."""
    app.dependency_overrides[RestaurantService] = lambda: restaurant_service
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def client():
    """Returns a test client for the FastAPI app."""
    from app.main import app
    from fastapi.testclient import TestClient
    return TestClient(app)

# region Restaurant Fixtures
@pytest.fixture
def valid_restaurant_payload():
    """Returns valid raw restaurant data for testing."""
    return {
        "name": "Test Restaurant",
        "cuisine": "Italian",
        "address": "123 Test St",
        "postalcode": "A1B2C3",
        "phone": "123-456-7890",
        "rating": 4.5,
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
def valid_restaurant_filter():
    """Returns a valid RestaurantFilter object for testing."""
    return RestaurantFilter(cuisine="Italian", city="Test City", province="Test Province")

@pytest.fixture
def restaurants_json(tmp_path):
    """Creates a temporary JSON file with restaurant data for testing."""
    data = [
        {
            "id": 1,
            "name": "Test Restaurant 1",
            "cuisine": "Italian",
            "address": "123 Test St",
            "postalcode": "A1B2C3",
            "phone": "123-456-7890",
            "rating": 4.5,
            "location": {
                "city": "Test City",
                "province": "Test Province"
            },
            "menu": [
                {
                    "id": 1,
                    "name": "Test Soup",
                    "description": "A test soup",
                    "price": 5.99,
                    "category": "Starters",
                    "image": "",
                    "availability": True
                },
                {
                    "id": 2,
                    "name": "Test Pasta",
                    "description": "A test pasta",
                    "price": 12.50,
                    "category": "Pasta",
                    "image": "",
                    "availability": True
                }
            ]
        },
        {
            "id": 2,
            "name": "Test Restaurant 2",
            "cuisine": "Mexican",
            "address": "456 Test Ave",
            "postalcode": "D4E5F6",
            "phone": "987-654-3210",
            "rating": 4.0,
            "location": {
                "city": "Another City",
                "province": "Another Province"
            },
            "menu": []
        },
        {
            "id": 3,
            "name": "Test Restaurant 3",
            "cuisine": "Italian",
            "address": "789 Test Rd",
            "postalcode": "G7H8I9",
            "phone": "555-123-4567",
            "rating": 3.2,
            "location": {
                "city": "Yet Another City",
                "province": "Another Province"
            },
            "menu": []
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
def valid_menu_item_payload():
    """Returns valid menu item data for testing."""
    return {
        "name": "Test Item",
        "price": 9.99,
        "category": "Burgers",
        "image": "http://example.com/image.jpg",
        "availability": True
    }

@pytest.fixture
def valid_menu_item_create(valid_menu_item_payload):
    """Returns a valid ItemCreate object for testing."""
    return ItemCreate(**valid_menu_item_payload)

@pytest.fixture
def restaurant_filter():
    """Factory fixture to create RestaurantFilter instances with custom parameters."""
    def _create_filter(**kwargs):
        return RestaurantFilter(**kwargs)
    return _create_filter
# endregion

# region User Fixtures
@pytest.fixture
def valid_user_payload():
    """Returns valid raw user data for testing."""
    return {
        "firstname": "Brady",
        "lastname": "Bracken",
        "email": "bradyryanbracken@gmail.com",
        "phone": "2508638425",
        "address": {
            "street": "613 Clifton Court",
            "city": "Kelowna",
            "province": "BC",
            "postalcode": "V1V0B7"
        },
        "is_active": True
    }