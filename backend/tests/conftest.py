import json

import pytest
from app.main import app
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.menu_item import ItemCreate
from app.schemas.restaurant import RestaurantCreate, RestaurantFilter
from app.services.restaurant_service import RestaurantService


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

@pytest.fixture(autouse=True)
def override_restaurant_dependency(restaurant_service):
    """Overrides the FastAPI service dependency to use the test repository fixture."""
    app.dependency_overrides[RestaurantService] = lambda: restaurant_service
    yield
    app.dependency_overrides.clear()
# endregion

# region User Fixtures
@pytest.fixture
def valid_user_payload():
    """Returns valid raw user data for testing."""
    return {
        "firstname": "Brady",
        "lastname": "Bracken",
        "password": "SecurePassword123!",
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

@pytest.fixture
def valid_user_create(valid_user_payload):
    """Returns a valid UserCreate Pydantic model instance."""
    from app.schemas.user import UserCreate
    return UserCreate(**valid_user_payload)

@pytest.fixture
def valid_user_update():
    """Returns a valid UserUpdate instance for partial updates."""
    from app.schemas.user import UserUpdate
    return UserUpdate(firstname="UpdatedName", is_active=False)

@pytest.fixture
def users_json(tmp_path):
    """Creates a temporary JSON file with sample user data for isolated testing."""
    import json

    from app.core.security import get_password_hash

    data = [
        {
            "id": 1,
            "role": "customer",
            "firstname": "John",
            "lastname": "Doe",
            "email": "john.doe@example.com",
            "password_hash": get_password_hash("SecurePassword123!"),
            "role": "customer",
            "phone": "2505550100",
            "address": {
                "street": "100 Main St",
                "city": "Kelowna",
                "province": "BC",
                "postalcode": "V1Y1Y1"
            },
            "is_active": True,
            "created_at": "2026-01-01T00:00:00Z",
            "last_updated": "2026-01-01T00:00:00Z"
        }
    ]
    file_path = tmp_path / "users.json"
    with open(file_path, "w") as f:
        json.dump(data, f)
    return str(file_path)

@pytest.fixture
def user_repository(users_json):
    """Returns a UserRepository instance using the temporary JSON file."""
    from app.repositories.user_repository import UserRepository
    return UserRepository(file_path=users_json)

@pytest.fixture
def user_service(user_repository):
    """Returns a UserService instance injected with the test repository."""
    from app.services.user_service import UserService
    service = UserService(user_repository=user_repository)
    return service

@pytest.fixture
def login_user():
    """Returns a user with a valid password for login tests."""
    from app.core.security import get_password_hash

    return {
        "id": 1,
        "email": "john.doe@example.com",
        "password_hash": get_password_hash("SecurePassword123!"),
        "is_active": True,
    }

@pytest.fixture
def login_repository(login_user):
    """Returns a repository that looks up the login test user by email."""
    class LoginRepository:
        def get_user_by_email(self, email):
            return login_user if email == login_user["email"] else None

    return LoginRepository()

@pytest.fixture
def login_service(login_repository):
    """Returns a LoginService using the login test repository."""
    from app.services.login_service import LoginService
    return LoginService(login_repository)

@pytest.fixture
def auth_headers():
    """Returns bearer headers for the first test user."""
    from app.core.security import create_access_token

    return {"Authorization": f"Bearer {create_access_token(1)}"}

@pytest.fixture(autouse=True)
def override_user_dependency(user_service):
    """Overrides the FastAPI user service dependency for route tests."""
    from app.main import app
    from app.services.user_service import UserService

    from app.api.routes import users
    from app.core.dependencies import get_user_repository

    user_dependency = getattr(users, "get_user_service", UserService)
    app.dependency_overrides[user_dependency] = lambda: user_service
    app.dependency_overrides[get_user_repository] = lambda: user_service.user_repository
    yield
    app.dependency_overrides.clear()
    
# endregion