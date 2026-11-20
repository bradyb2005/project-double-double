import json

import pytest
from app.main import app
from app.repositories.order_repository import OrderRepository
from app.routes.orders import get_order_service
from app.services.order_service import OrderService
from fastapi import status


def make_order(order_id, customer_id, created_at, status_value="pending"):
    return {
        "id": order_id,
        "customer_id": customer_id,
        "customer_details": {
            "firstname": "John",
            "lastname": "Doe",
            "email": "john.doe@example.com",
            "phone": "2505550100",
            "address": {
                "street": "100 Main St",
                "city": "Kelowna",
                "province": "BC",
                "postalcode": "V1Y1Y1",
            },
        },
        "restaurant_id": 1,
        "items": [
            {"item_id": 1, "name": "Test Soup", "price": 5.99, "quantity": 2},
            {"item_id": 2, "name": "Test Pasta", "price": 12.5, "quantity": 1},
        ],
        "total_price": 24.48,
        "status": status_value,
        "created_at": created_at,
    }


@pytest.fixture
def orders_json(tmp_path):
    data = [
        make_order(1, 1, "2026-11-01T12:00:00+00:00", "delivered"),
        make_order(2, 2, "2026-11-02T12:00:00+00:00"),
        make_order(3, 1, "2026-11-03T12:00:00+00:00"),
    ]
    file_path = tmp_path / "orders.json"
    file_path.write_text(json.dumps(data))
    return str(file_path)


@pytest.fixture
def order_repository(orders_json):
    return OrderRepository(file_path=orders_json)


@pytest.fixture(autouse=True)
def override_dependency(order_repository, user_repository, restaurant_repository, cart_service):
    service = OrderService(
        user_repository=user_repository,
        restaurant_repository=restaurant_repository,
        order_repository=order_repository,
        cart_service=cart_service,
    )
    app.dependency_overrides[get_order_service] = lambda: service
    yield
    app.dependency_overrides.pop(get_order_service, None)


class TestListOrders:
    def test_list_orders_requires_authentication(self, client):
        response = client.get("/users/1/orders")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_orders_requires_same_user(self, client, auth_headers):
        response = client.get("/users/2/orders", headers=auth_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_orders_returns_only_own_orders_newest_first(self, client, auth_headers):
        response = client.get("/users/1/orders", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert [order["id"] for order in data] == [3, 1]
        assert all(order["customer_id"] == 1 for order in data)

    def test_list_orders_includes_current_and_past(self, client, auth_headers):
        response = client.get("/users/1/orders", headers=auth_headers)
        statuses = {order["status"] for order in response.json()}
        assert statuses == {"pending", "delivered"}

    def test_list_orders_empty(self, client, auth_headers, orders_json):
        with open(orders_json, "w") as f:
            json.dump([], f)
        response = client.get("/users/1/orders", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []


class TestGetOrder:
    def test_get_order_requires_authentication(self, client):
        response = client.get("/users/1/orders/3")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_order_requires_same_user(self, client, auth_headers):
        response = client.get("/users/2/orders/2", headers=auth_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_order_returns_details(self, client, auth_headers):
        response = client.get("/users/1/orders/3", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 3
        assert data["status"] == "pending"
        assert data["total_price"] == 24.48
        assert data["items"] == [
            {"item_id": 1, "name": "Test Soup", "price": 5.99, "quantity": 2},
            {"item_id": 2, "name": "Test Pasta", "price": 12.5, "quantity": 1},
        ]

    def test_get_order_of_another_customer_is_not_found(self, client, auth_headers):
        response = client.get("/users/1/orders/2", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Order with ID 2 not found."

    def test_get_missing_order_is_not_found(self, client, auth_headers):
        response = client.get("/users/1/orders/999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_order_invalid_id_type(self, client, auth_headers):
        response = client.get("/users/1/orders/abc", headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_checkout_path_still_posts(self, client, auth_headers):
        response = client.post("/users/1/orders/checkout", headers=auth_headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
