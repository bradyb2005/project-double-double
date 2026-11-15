import pytest
from app.main import app
from app.repositories.user_repository import UserRepository
from app.routes.carts import get_cart_service
from fastapi import status


@pytest.fixture(autouse=True)
def override_dependency(cart_service, users_json, monkeypatch):
    save_users = UserRepository.save_users

    def save_test_users(repository, users):
        assert str(repository.filePath) == users_json, "Refusing to write outside test users file"
        return save_users(repository, users)

    monkeypatch.setattr(UserRepository, "save_users", save_test_users)
    app.dependency_overrides[get_cart_service] = lambda: cart_service
    yield
    app.dependency_overrides.pop(get_cart_service, None)


class TestGetCart:
    def test_get_cart_requires_authentication(self, client):
        response = client.get("/users/1/cart")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_cart_requires_same_user(self, client, auth_headers):
        response = client.get("/users/99999/cart", headers=auth_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_cart_success(self, client, auth_headers):
        response = client.get("/users/1/cart", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert isinstance(data["items"], list)

    def test_get_cart_returns_empty_cart(self, client, auth_headers):
        response = client.get("/users/1/cart", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0.0

    def test_get_cart_invalid_user_id_type(self, client, auth_headers):
        response = client.get("/users/abc/cart", headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_get_cart_rejects_invalid_token(self, client):
        response = client.get(
            "/users/1/cart",
            headers={"Authorization": "Bearer invalid"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAddToCart:
    def test_add_to_cart_requires_authentication(self, client):
        payload = {"item_id": 1, "restaurant_id": 1, "quantity": 1}
        response = client.post("/users/1/cart/items", json=payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_add_to_cart_requires_same_user(self, client, auth_headers):
        payload = {"item_id": 1, "restaurant_id": 1, "quantity": 1}
        response = client.post("/users/99999/cart/items", json=payload, headers=auth_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_add_to_cart_success(self, client, auth_headers):
        payload = {"item_id": 1, "restaurant_id": 1, "quantity": 2}
        response = client.post("/users/1/cart/items", json=payload, headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["item_id"] == 1
        assert data["items"][0]["quantity"] == 2
        assert data["total"] == 11.98

    def test_add_to_cart_persists_to_test_repository(self, client, auth_headers, user_repository):
        payload = {"item_id": 1, "restaurant_id": 1, "quantity": 2}
        response = client.post("/users/1/cart/items", json=payload, headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert user_repository.get_user_by_id(1)["cart"] == response.json()

    def test_add_to_cart_with_invalid_restaurant_raises_error(self, client, auth_headers):
        payload = {"item_id": 1, "restaurant_id": 999, "quantity": 1}
        response = client.post("/users/1/cart/items", json=payload, headers=auth_headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_add_to_cart_with_invalid_menu_item_raises_error(self, client, auth_headers):
        payload = {"item_id": 999, "restaurant_id": 1, "quantity": 1}
        response = client.post("/users/1/cart/items", json=payload, headers=auth_headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_add_to_cart_with_zero_quantity_raises_error(self, client, auth_headers):
        payload = {"item_id": 1, "restaurant_id": 1, "quantity": 0}
        response = client.post("/users/1/cart/items", json=payload, headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_add_to_cart_with_negative_quantity_raises_error(self, client, auth_headers):
        payload = {"item_id": 1, "restaurant_id": 1, "quantity": -5}
        response = client.post("/users/1/cart/items", json=payload, headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_add_to_cart_different_restaurant_raises_error(self, client, auth_headers):
        # Add item from restaurant 1
        payload1 = {"item_id": 1, "restaurant_id": 1, "quantity": 1}
        response1 = client.post("/users/1/cart/items", json=payload1, headers=auth_headers)
        assert response1.status_code == status.HTTP_200_OK

        # Try to add item from restaurant 2
        payload2 = {"item_id": 1, "restaurant_id": 2, "quantity": 1}
        response2 = client.post("/users/1/cart/items", json=payload2, headers=auth_headers)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert "different restaurants" in response2.json()["detail"].lower()

    def test_add_to_cart_duplicate_item_increases_quantity(self, client, auth_headers):
        # Add item once
        payload = {"item_id": 1, "restaurant_id": 1, "quantity": 1}
        response1 = client.post("/users/1/cart/items", json=payload, headers=auth_headers)
        assert response1.status_code == status.HTTP_200_OK

        # Add same item again with different quantity
        payload = {"item_id": 1, "restaurant_id": 1, "quantity": 2}
        response2 = client.post("/users/1/cart/items", json=payload, headers=auth_headers)
        assert response2.status_code == status.HTTP_200_OK
        data = response2.json()
        assert data["items"] == [{"item_id": 1, "restaurant_id": 1, "quantity": 3}]
        assert data["total"] == pytest.approx(17.97)
        assert client.get("/users/1/cart", headers=auth_headers).json() == data

    def test_add_to_cart_missing_required_fields(self, client, auth_headers):
        payload = {"item_id": 1}  # Missing restaurant_id and quantity
        response = client.post("/users/1/cart/items", json=payload, headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_add_to_cart_invalid_user_id_type(self, client, auth_headers):
        payload = {"item_id": 1, "restaurant_id": 1, "quantity": 1}
        response = client.post("/users/abc/cart/items", json=payload, headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_add_to_cart_calculates_total_correctly(self, client, auth_headers):
        # Add first item: 5.99
        payload1 = {"item_id": 1, "restaurant_id": 1, "quantity": 1}
        response1 = client.post("/users/1/cart/items", json=payload1, headers=auth_headers)
        assert response1.json()["total"] == 5.99

        # Add second item: 12.50
        payload2 = {"item_id": 2, "restaurant_id": 1, "quantity": 1}
        response2 = client.post("/users/1/cart/items", json=payload2, headers=auth_headers)
        assert response2.json()["total"] == pytest.approx(18.49)


class TestUpdateCartItem:
    def test_update_cart_item_requires_authentication(self, client):
        response = client.put(
            "/users/1/cart/items/1?quantity=5",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_cart_item_requires_same_user(self, client, auth_headers):
        response = client.put(
            "/users/99999/cart/items/1?quantity=5",
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_cart_item_success(self, client, auth_headers):
        # Add item first
        add_payload = {"item_id": 1, "restaurant_id": 1, "quantity": 1}
        client.post("/users/1/cart/items", json=add_payload, headers=auth_headers)

        # Update quantity
        response = client.put(
            "/users/1/cart/items/1?quantity=3",
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["items"][0]["quantity"] == 3
        assert data["total"] == 17.97  # 5.99 * 3

    def test_update_cart_item_not_found_raises_error(self, client, auth_headers):
        response = client.put(
            "/users/1/cart/items/999?quantity=5",
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_cart_item_requires_quantity(self, client, auth_headers):
        response = client.put("/users/1/cart/items/1", headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_update_cart_item_with_zero_quantity_raises_error(self, client, auth_headers):
        # Add item first
        add_payload = {"item_id": 1, "restaurant_id": 1, "quantity": 1}
        client.post("/users/1/cart/items", json=add_payload, headers=auth_headers)

        # Try to update with zero quantity
        response = client.put(
            "/users/1/cart/items/1?quantity=0",
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_update_cart_item_with_negative_quantity_raises_error(self, client, auth_headers):
        # Add item first
        add_payload = {"item_id": 1, "restaurant_id": 1, "quantity": 1}
        client.post("/users/1/cart/items", json=add_payload, headers=auth_headers)

        # Try to update with negative quantity
        response = client.put(
            "/users/1/cart/items/1?quantity=-5",
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_update_cart_item_recalculates_total(self, client, auth_headers):
        # Add item with quantity 2
        add_payload = {"item_id": 1, "restaurant_id": 1, "quantity": 2}
        response1 = client.post("/users/1/cart/items", json=add_payload, headers=auth_headers)
        assert response1.json()["total"] == 11.98

        # Update to quantity 5
        response2 = client.put(
            "/users/1/cart/items/1?quantity=5",
            headers=auth_headers,
        )
        assert response2.json()["total"] == pytest.approx(29.95)


class TestRemoveFromCart:
    def test_remove_from_cart_requires_authentication(self, client):
        response = client.delete("/users/1/cart/items/1")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_remove_from_cart_requires_same_user(self, client, auth_headers):
        response = client.delete(
            "/users/99999/cart/items/1",
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_remove_from_cart_success(self, client, auth_headers):
        # Add two items
        add_payload1 = {"item_id": 1, "restaurant_id": 1, "quantity": 1}
        add_payload2 = {"item_id": 2, "restaurant_id": 1, "quantity": 1}
        client.post("/users/1/cart/items", json=add_payload1, headers=auth_headers)
        client.post("/users/1/cart/items", json=add_payload2, headers=auth_headers)

        # Remove first item
        response = client.delete("/users/1/cart/items/1", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["item_id"] == 2
        assert data["total"] == 12.50

    def test_remove_from_cart_item_not_found(self, client, auth_headers):
        response = client.delete("/users/1/cart/items/999", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK  # Doesn't error, just empty
        data = response.json()
        assert data["items"] == []

    def test_remove_from_cart_recalculates_total(self, client, auth_headers):
        # Add two items
        add_payload1 = {"item_id": 1, "restaurant_id": 1, "quantity": 2}  # 11.98
        add_payload2 = {"item_id": 2, "restaurant_id": 1, "quantity": 1}  # 12.50
        client.post("/users/1/cart/items", json=add_payload1, headers=auth_headers)
        response_before = client.post("/users/1/cart/items", json=add_payload2, headers=auth_headers)
        assert response_before.json()["total"] == 24.48

        # Remove first item
        response_after = client.delete("/users/1/cart/items/1", headers=auth_headers)
        assert response_after.json()["total"] == 12.50

    def test_remove_from_cart_invalid_user_id_type(self, client, auth_headers):
        response = client.delete("/users/abc/cart/items/1", headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


class TestClearCart:
    def test_clear_cart_requires_authentication(self, client):
        response = client.delete("/users/1/cart")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_clear_cart_requires_same_user(self, client, auth_headers):
        response = client.delete("/users/99999/cart", headers=auth_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_clear_cart_success(self, client, auth_headers):
        # Add items
        add_payload1 = {"item_id": 1, "restaurant_id": 1, "quantity": 1}
        add_payload2 = {"item_id": 2, "restaurant_id": 1, "quantity": 2}
        client.post("/users/1/cart/items", json=add_payload1, headers=auth_headers)
        client.post("/users/1/cart/items", json=add_payload2, headers=auth_headers)

        # Clear cart
        response = client.delete("/users/1/cart", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0.0

    def test_clear_empty_cart(self, client, auth_headers):
        response = client.delete("/users/1/cart", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0.0

    def test_clear_cart_invalid_user_id_type(self, client, auth_headers):
        response = client.delete("/users/abc/cart", headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
