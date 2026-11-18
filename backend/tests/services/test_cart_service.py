import pytest
from app.services.cart_service import CartService


@pytest.fixture
def cart_with_items():
    """Returns a cart with items for testing."""
    from app.schemas.cart import Cart, CartItem

    return Cart(
        items=[
            CartItem(item_id=1, restaurant_id=101, quantity=2),
            CartItem(item_id=2, restaurant_id=101, quantity=1),
        ],
        subtotal=30.0,
    )

@pytest.fixture
def cart_service(user_repository, restaurant_repository):
    """Returns a cart service using the test repositories."""
    service = CartService(user_repository)
    service.restaurant_repository = restaurant_repository
    return service

class TestGetCart:
    def test_get_cart_returns_existing_cart(self, cart_service):
        cart = cart_service.get_cart(1)

        assert cart.items == []
        assert cart.subtotal == 0.0

    def test_get_cart_invalid_user_raises(self, cart_service):
        with pytest.raises(ValueError, match="User not found"):
            cart_service.get_cart(999)

    def test_get_cart_combines_existing_duplicate_items(self, cart_service, user_repository):
        user_repository.update_cart(1, {
            "items": [
                {"item_id": 1, "restaurant_id": 1, "quantity": 1},
                {"item_id": 2, "restaurant_id": 1, "quantity": 1},
                {"item_id": 1, "restaurant_id": 1, "quantity": 2},
            ],
            "subtotal": 30.47,
        })

        cart = cart_service.get_cart(1)

        assert [(item.item_id, item.quantity) for item in cart.items] == [(1, 3), (2, 1)]
        assert cart.subtotal == 30.47


class TestAddToCart:
    def test_add_to_cart_adds_item(self, cart_service):
        updated_cart = cart_service.add_to_cart(1, item_id=1, restaurant_id=1, quantity=1)

        assert any(item.item_id == 1 for item in updated_cart.items)
        assert updated_cart.subtotal == 5.99

    def test_add_to_cart_different_restaurant_raises(self, cart_service):
        cart_service.add_to_cart(1, item_id=1, restaurant_id=1, quantity=1)

        with pytest.raises(ValueError, match="Cannot add items from different restaurants"):
            cart_service.add_to_cart(1, item_id=1, restaurant_id=2, quantity=1)

    def test_add_to_cart_invalid_user_raises(self, cart_service):
        with pytest.raises(ValueError, match="User not found"):
            cart_service.add_to_cart(999, item_id=1, restaurant_id=1, quantity=1)

    def test_add_to_cart_invalid_quantity_raises(self, cart_service):
        with pytest.raises(ValueError, match="greater than 0"):
            cart_service.add_to_cart(1, item_id=1, restaurant_id=1, quantity=0)

    def test_add_to_existing_item_invalid_quantity_raises(self, cart_service):
        cart_service.add_to_cart(1, item_id=1, restaurant_id=1, quantity=1)

        with pytest.raises(ValueError, match="greater than 0"):
            cart_service.add_to_cart(1, item_id=1, restaurant_id=1, quantity=0)

        assert cart_service.get_cart(1).items[0].quantity == 1

    def test_add_to_cart_duplicate_item_updates_quantity(self, cart_service):
        cart_service.add_to_cart(1, item_id=1, restaurant_id=1, quantity=1)
        updated_cart = cart_service.add_to_cart(1, item_id=1, restaurant_id=1, quantity=2)

        assert [item.quantity for item in updated_cart.items if item.item_id == 1] == [3]
        assert updated_cart.subtotal == pytest.approx(17.97)
        assert cart_service.get_cart(1) == updated_cart

    def test_add_to_cart_combines_existing_duplicate_items(self, cart_service, user_repository):
        user_repository.update_cart(1, {
            "items": [
                {"item_id": 1, "restaurant_id": 1, "quantity": 1},
                {"item_id": 1, "restaurant_id": 1, "quantity": 2},
            ],
            "subtotal": 17.97,
        })

        cart = cart_service.add_to_cart(1, item_id=1, restaurant_id=1, quantity=2)

        assert [(item.item_id, item.quantity) for item in cart.items] == [(1, 5)]
        assert cart.subtotal == pytest.approx(29.95)
        assert user_repository.get_user_by_id(1)["cart"] == cart.model_dump(mode="json")
    def test_add_to_cart_unavailable_item_raises(self, cart_service, restaurant_repository):
        restaurants = restaurant_repository.get_all_restaurants()
        restaurants[0]["menu"][1]["availability"] = False  # item 2 (Test Pasta)
        restaurant_repository.save_restaurants(restaurants)

        with pytest.raises(ValueError, match="not available"):
            cart_service.add_to_cart(1, item_id=2, restaurant_id=1, quantity=1)

        assert cart_service.get_cart(1).items == []

    def test_add_to_cart_available_item_still_works_when_another_is_unavailable(
        self, cart_service, restaurant_repository
    ):
        restaurants = restaurant_repository.get_all_restaurants()
        restaurants[0]["menu"][1]["availability"] = False  # item 2 (Test Pasta)
        restaurant_repository.save_restaurants(restaurants)

        cart = cart_service.add_to_cart(1, item_id=1, restaurant_id=1, quantity=1)

        assert [(item.item_id, item.quantity) for item in cart.items] == [(1, 1)]

    def test_add_to_cart_inactive_user_raises(self, cart_service, user_repository):
        user_repository.update_user(1, {"is_active": False})

        with pytest.raises(ValueError, match="Inactive customers"):
            cart_service.add_to_cart(1, item_id=1, restaurant_id=1, quantity=1)

        assert cart_service.get_cart(1).items == []

    def test_add_to_cart_active_user_still_works(self, cart_service, user_repository):
        user_repository.update_user(1, {"is_active": True})

        cart = cart_service.add_to_cart(1, item_id=1, restaurant_id=1, quantity=1)

        assert [(item.item_id, item.quantity) for item in cart.items] == [(1, 1)]

class TestUpdateCart:
    def test_update_combines_existing_duplicate_items(self, cart_service, user_repository):
        user_repository.update_cart(1, {
            "items": [
                {"item_id": 1, "restaurant_id": 1, "quantity": 1},
                {"item_id": 2, "restaurant_id": 1, "quantity": 1},
                {"item_id": 1, "restaurant_id": 1, "quantity": 2},
            ],
            "subtotal": 30.47,
        })

        cart = cart_service.update_cart_item(1, item_id=1, new_quantity=4)

        assert [(item.item_id, item.quantity) for item in cart.items] == [(1, 4), (2, 1)]
        assert cart.subtotal == pytest.approx(36.46)
        assert user_repository.get_user_by_id(1)["cart"] == cart.model_dump(mode="json")

class TestInactiveUserCannotModifyCart:
    def test_inactive_user_cannot_remove_update_or_clear(self, cart_service, user_repository):
        cart_service.add_to_cart(1, item_id=1, restaurant_id=1, quantity=1)
        user_repository.update_user(1, {"is_active": False})

        with pytest.raises(ValueError, match="Inactive customers"):
            cart_service.remove_from_cart(1, 1)
        with pytest.raises(ValueError, match="Inactive customers"):
            cart_service.update_cart_item(1, 1, 3)
        with pytest.raises(ValueError, match="Inactive customers"):
            cart_service.clear_cart(1)

        assert [(i.item_id, i.quantity) for i in cart_service.get_cart(1).items] == [(1, 1)]

class TestInvalidQuantities:
    @pytest.mark.parametrize("quantity", [0, -1, 1.5])
    def test_add_to_cart_rejects_invalid_quantity(self, cart_service, quantity):
        with pytest.raises(ValueError):
            cart_service.add_to_cart(1, item_id=1, restaurant_id=1, quantity=quantity)

        assert cart_service.get_cart(1).items == []

    @pytest.mark.parametrize("quantity", [0, -1, 1.5])
    def test_update_cart_item_rejects_invalid_quantity(self, cart_service, quantity):
        cart_service.add_to_cart(1, item_id=1, restaurant_id=1, quantity=2)

        with pytest.raises(ValueError):
            cart_service.update_cart_item(1, 1, quantity)

        assert cart_service.get_cart(1).items[0].quantity == 2


# class TestRemoveFromCart:
 
# class TestClearCart:
