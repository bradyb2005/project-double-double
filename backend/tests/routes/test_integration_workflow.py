"""
Integration tests demonstrating the complete customer workflow:
Customer Registration → Browse Restaurants → Add to Cart → Checkout → Order Created
"""

import json

import pytest
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
def override_dependencies(order_repository, user_repository, restaurant_repository, cart_service):
    """Override dependencies to use test repositories."""
    app.dependency_overrides[get_order_service] = lambda: OrderService(
        user_repository=user_repository,
        restaurant_repository=restaurant_repository,
        order_repository=order_repository,
        cart_service=cart_service,
    )
    yield
    app.dependency_overrides.pop(get_order_service, None)


class TestIntegrationCustomerWorkflow:
    """Full integration test: Customer workflow from registration to order creation."""

    def test_complete_workflow_register_browse_add_checkout_order(
        self, client, user_repository, restaurant_repository, cart_service
    ):
        """
        End-to-end workflow test demonstrating the complete customer workflow:
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
        response = client.post("/users", json=register_payload)
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
            json={"item_id": item_1["id"], "quantity": 2, "restaurant_id": restaurant_id},
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
            json={"item_id": item_2["id"], "quantity": 1, "restaurant_id": restaurant_id},
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

    def test_workflow_add_to_cart_and_checkout_basic(self, client, auth_headers):
        """
        Test a simpler workflow: add items to existing user cart and checkout.
        """

        # Add item to cart for user 1
        response = client.post(
            "/users/1/cart/items",
            json={"item_id": 1, "quantity": 2, "restaurant_id": 1},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        cart = response.json()
        assert len(cart["items"]) == 1
        assert cart["subtotal"] == 11.98

        # View cart
        response = client.get("/users/1/cart", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        cart = response.json()
        assert len(cart["items"]) == 1
        assert cart["subtotal"] == 11.98

        # Checkout
        response = client.post("/users/1/orders", headers=auth_headers)
        assert response.status_code == status.HTTP_201_CREATED
        order = response.json()
        assert order["customer_id"] == 1
        assert len(order["items"]) == 1
        assert order["items"][0]["item_id"] == 1

        # Verify cart cleared
        response = client.get("/users/1/cart", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        cart = response.json()
        assert len(cart["items"]) == 0

    def test_workflow_single_restaurant_requirement(self, client, auth_headers):
        """
        Test that a cart can contain items from only ONE restaurant.
        Attempting to add items from a second restaurant should fail.
        """

        # Add item from restaurant 1
        response = client.post(
            "/users/1/cart/items",
            json={"item_id": 1, "quantity": 1, "restaurant_id": 1},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK

        # Try to add item from different restaurant (should fail)
        response = client.post(
            "/users/1/cart/items",
            json={"item_id": 1, "quantity": 1, "restaurant_id": 2},
            headers=auth_headers,
        )
        # Should fail because item is from different restaurant
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = response.json()
        assert "restaurant" in error["detail"].lower()
