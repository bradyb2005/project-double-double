"""
Integration tests demonstrating the complete customer workflow:
Customer Registration → Browse Restaurants → Add to Cart → Checkout → Order Created
"""

import json

import pytest
from app.core.security import create_access_token
from app.main import app
from app.repositories.order_repository import OrderRepository
from app.routes.orders import get_order_service
from app.services.order_service import OrderService
from fastapi import status


@pytest.fixture
def orders_json(tmp_path):
    """Creates a temporary JSON file for orders (starts empty)."""
    file_path = tmp_path / "orders.json"
    file_path.write_text(json.dumps([]))
    return str(file_path)


@pytest.fixture
def order_repository(orders_json):
    """Returns an OrderRepository instance using the temporary JSON file."""
    return OrderRepository(file_path=orders_json)


@pytest.fixture(autouse=True)
def override_order_dependency(order_repository, user_repository, restaurant_repository, cart_service):
    """Overrides the FastAPI order service dependency for route tests."""
    service = OrderService(
        user_repository=user_repository,
        restaurant_repository=restaurant_repository,
        order_repository=order_repository,
        cart_service=cart_service,
    )
    app.dependency_overrides[get_order_service] = lambda: service
    yield
    app.dependency_overrides.pop(get_order_service, None)


class TestIntegrationCustomerWorkflow:
    """Full integration test: Customer workflow from registration to order creation."""

    def test_complete_workflow_register_browse_add_checkout_order(
        self, client, user_repository, restaurant_repository, cart_service
    ):
        """
        End-to-end workflow test demonstrating:
        1. Customer registration
        2. Customer login
        3. Browse restaurants
        4. Browse menu items
        5. Add items to cart
        6. View cart
        7. Checkout and create order
        8. Verify order was created
        9. Verify cart was cleared
        """

        # ===== STEP 1: Register a new customer =====
        register_payload = {
            "firstname": "Alice",
            "lastname": "Smith",
            "email": "alice.smith@example.com",
            "password": "SecurePassword123!",
            "phone": "2501234567",
            "address": {
                "street": "999 Integration Lane",
                "city": "Kelowna",
                "province": "BC",
                "postalcode": "V1V1V1",
            },
        }
        response = client.post("/users/register", json=register_payload)
        assert response.status_code == status.HTTP_201_CREATED
        user_data = response.json()
        new_user_id = user_data["id"]
        assert user_data["firstname"] == "Alice"
        assert user_data["email"] == "alice.smith@example.com"
        assert user_data["is_active"] is True

        # ===== STEP 2: Login with the new customer =====
        login_payload = {
            "email": "alice.smith@example.com",
            "password": "SecurePassword123!",
        }
        response = client.post("/login", json=login_payload)
        assert response.status_code == status.HTTP_200_OK
        login_data = response.json()
        assert "access_token" in login_data
        auth_token = login_data["access_token"]
        auth_headers = {"Authorization": f"Bearer {auth_token}"}

        # ===== STEP 3: Browse restaurants =====
        response = client.get("/restaurants")
        assert response.status_code == status.HTTP_200_OK
        restaurants = response.json()
        assert len(restaurants) > 0
        restaurant_id = restaurants[0]["id"]  # Pick the first restaurant
        assert restaurants[0]["id"] == 1
        assert restaurants[0]["name"] == "Test Restaurant 1"

        # ===== STEP 4: Get restaurant details and browse menu =====
        response = client.get(f"/restaurants/{restaurant_id}")
        assert response.status_code == status.HTTP_200_OK
        restaurant_detail = response.json()
        assert "menu" in restaurant_detail
        menu_items = restaurant_detail["menu"]
        assert len(menu_items) >= 2
        item_1 = menu_items[0]
        item_2 = menu_items[1]
        assert item_1["id"] == 1
        assert item_1["name"] == "Test Soup"
        assert item_1["price"] == 5.99
        assert item_1["availability"] is True

        # ===== STEP 5: Add items to cart =====
        # Add first item (qty 2)
        response = client.post(
            f"/users/{new_user_id}/cart/items",
            json={"item_id": item_1["id"], "quantity": 2},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        cart = response.json()
        assert len(cart["items"]) == 1
        assert cart["items"][0]["item_id"] == item_1["id"]
        assert cart["items"][0]["quantity"] == 2
        assert cart["items"][0]["restaurant_id"] == restaurant_id

        # Add second item (qty 1)
        response = client.post(
            f"/users/{new_user_id}/cart/items",
            json={"item_id": item_2["id"], "quantity": 1},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        cart = response.json()
        assert len(cart["items"]) == 2
        item_ids = {item["item_id"] for item in cart["items"]}
        assert item_ids == {item_1["id"], item_2["id"]}

        # ===== STEP 6: View current cart =====
        response = client.get(f"/users/{new_user_id}/cart", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        current_cart = response.json()
        assert len(current_cart["items"]) == 2
        # Verify totals are calculated
        assert current_cart["subtotal"] is not None
        assert current_cart["tax"] is not None
        assert current_cart["total"] is not None
        # Expected: (5.99 * 2) + (12.50 * 1) = 11.98 + 12.50 = 24.48 subtotal
        assert current_cart["subtotal"] == 24.48

        # ===== STEP 7: Checkout and create order =====
        response = client.post(f"/users/{new_user_id}/orders", headers=auth_headers)
        assert response.status_code == status.HTTP_201_CREATED
        order = response.json()
        order_id = order["id"]
        assert order["customer_id"] == new_user_id
        assert order["restaurant_id"] == restaurant_id
        assert len(order["items"]) == 2
        assert order["status"] == "pending"
        assert order["total_price"] is not None
        # Verify order contains the items we added
        order_item_ids = {item["item_id"] for item in order["items"]}
        assert order_item_ids == {item_1["id"], item_2["id"]}

        # ===== STEP 8: Retrieve the created order =====
        response = client.get(f"/users/{new_user_id}/orders/{order_id}", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        retrieved_order = response.json()
        assert retrieved_order["id"] == order_id
        assert retrieved_order["customer_id"] == new_user_id
        assert retrieved_order["status"] == "pending"

        # ===== STEP 9: Verify cart was cleared =====
        response = client.get(f"/users/{new_user_id}/cart", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        cleared_cart = response.json()
        assert len(cleared_cart["items"]) == 0
        assert cleared_cart["subtotal"] == 0.0
        assert cleared_cart["tax"] == 0.0
        assert cleared_cart["total"] == 0.0

    def test_workflow_reject_deactivated_customer_at_checkout(
        self, client, auth_headers, user_repository
    ):
        """
        Test that a deactivated customer cannot checkout,
        even if they have items in their cart.
        """

        # Setup: Deactivate user 1
        user = user_repository.get_user_by_id(1)
        user["is_active"] = False
        user_repository.save_user(user)

        # Add items to cart for deactivated user
        response = client.post(
            "/users/1/cart/items",
            json={"item_id": 1, "quantity": 1},
            headers=auth_headers,
        )
        # Should fail because user is deactivated
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY or response.status_code == status.HTTP_401_UNAUTHORIZED

        # Verify checkout also fails
        response = client.post("/users/1/orders", headers=auth_headers)
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_422_UNPROCESSABLE_ENTITY]

    def test_workflow_reject_unavailable_item_at_checkout(
        self, client, auth_headers, restaurant_repository
    ):
        """
        Test that unavailable menu items are rejected during checkout,
        even if they were available when added to cart.
        """

        # Setup: Add items to cart
        response = client.post(
            "/users/1/cart/items",
            json={"item_id": 1, "quantity": 1},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK

        # Simulate: Item becomes unavailable
        restaurant = restaurant_repository.get_restaurant_by_id(1)
        menu_item = next((item for item in restaurant["menu"] if item["id"] == 1), None)
        assert menu_item is not None
        menu_item["availability"] = False
        restaurant_repository.save_restaurant(restaurant)

        # Attempt checkout: Should fail because item is now unavailable
        response = client.post("/users/1/orders", headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        error = response.json()
        assert "unavailable" in error["detail"].lower()

    def test_workflow_prices_recalculated_at_checkout(
        self, client, auth_headers, restaurant_repository
    ):
        """
        Test that menu item prices are recalculated during checkout
        to reflect current prices, not cached prices from when items
        were added to cart.
        """

        # Setup: Add item to cart at current price (5.99)
        response = client.post(
            "/users/1/cart/items",
            json={"item_id": 1, "quantity": 1},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        cart = response.json()
        # Initial price should be 5.99
        assert any(item["item_id"] == 1 for item in cart["items"])

        # Simulate: Price changes in restaurant menu
        restaurant = restaurant_repository.get_restaurant_by_id(1)
        menu_item = next((item for item in restaurant["menu"] if item["id"] == 1), None)
        assert menu_item is not None
        original_price = menu_item["price"]
        menu_item["price"] = 10.99  # Change price
        restaurant_repository.save_restaurant(restaurant)

        # Checkout and verify order uses NEW price
        response = client.post("/users/1/orders", headers=auth_headers)
        assert response.status_code == status.HTTP_201_CREATED
        order = response.json()
        order_item = next((item for item in order["items"] if item["item_id"] == 1), None)
        assert order_item is not None
        assert order_item["price"] == 10.99  # New price, not old price

    def test_workflow_single_restaurant_requirement(
        self, client, auth_headers, user_repository, restaurant_repository
    ):
        """
        Test that a cart can contain items from only ONE restaurant.
        Attempting to add items from a second restaurant should fail.
        """

        # Setup: Add item from restaurant 1
        response = client.post(
            "/users/1/cart/items",
            json={"item_id": 1, "quantity": 1},  # Restaurant 1, Item 1
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK

        # Add item from restaurant 2 (should fail or replace cart)
        # First, verify restaurant 2 exists and has a menu
        restaurant_2 = restaurant_repository.get_restaurant_by_id(2)
        # Restaurant 2 has no menu items in test data, so let's add one
        menu_item = {
            "id": 100,
            "name": "Restaurant 2 Item",
            "price": 8.99,
            "category": "Test",
            "availability": True,
        }
        restaurant_2["menu"] = [menu_item]
        restaurant_repository.save_restaurant(restaurant_2)

        # Try to add item from different restaurant
        response = client.post(
            "/users/1/cart/items",
            json={"item_id": 100, "quantity": 1},  # Restaurant 2, Item 100
            headers=auth_headers,
        )
        # Should fail because item is from different restaurant
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        error = response.json()
        assert "restaurant" in error["detail"].lower()
