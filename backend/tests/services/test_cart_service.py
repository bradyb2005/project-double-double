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
        total=30.0,
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
        assert cart.total == 0.0

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
            "total": 30.47,
        })

        cart = cart_service.get_cart(1)

        assert [(item.item_id, item.quantity) for item in cart.items] == [(1, 3), (2, 1)]
        assert cart.total == 30.47


class TestAddToCart:
    def test_add_to_cart_adds_item(self, cart_service):
        updated_cart = cart_service.add_to_cart(1, item_id=1, restaurant_id=1, quantity=1)

        assert any(item.item_id == 1 for item in updated_cart.items)
        assert updated_cart.subtotal == 5.99
        assert updated_cart.total == 7.31

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
        assert updated_cart.total == pytest.approx(21.93)
        assert cart_service.get_cart(1) == updated_cart

    def test_add_to_cart_combines_existing_duplicate_items(self, cart_service, user_repository):
        user_repository.update_cart(1, {
            "items": [
                {"item_id": 1, "restaurant_id": 1, "quantity": 1},
                {"item_id": 1, "restaurant_id": 1, "quantity": 2},
            ],
            "total": 17.97,
        })

        cart = cart_service.add_to_cart(1, item_id=1, restaurant_id=1, quantity=2)

        assert [(item.item_id, item.quantity) for item in cart.items] == [(1, 5)]
        assert cart.subtotal == pytest.approx(29.95)
        assert cart.total == pytest.approx(36.55)
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
        

class TestUpdateCart:
    def test_update_combines_existing_duplicate_items(self, cart_service, user_repository):
        user_repository.update_cart(1, {
            "items": [
                {"item_id": 1, "restaurant_id": 1, "quantity": 1},
                {"item_id": 2, "restaurant_id": 1, "quantity": 1},
                {"item_id": 1, "restaurant_id": 1, "quantity": 2},
            ],
            "total": 30.47,
        })

        cart = cart_service.update_cart_item(1, item_id=1, new_quantity=4)

        assert [(item.item_id, item.quantity) for item in cart.items] == [(1, 4), (2, 1)]
        assert cart.subtotal == pytest.approx(36.46)
        assert cart.total == pytest.approx(44.48)
        assert user_repository.get_user_by_id(1)["cart"] == cart.model_dump(mode="json")

class TestCalculateCartTotals:
    def test_empty_cart_is_all_zero(self, cart_service):
        from app.schemas.cart import Cart

        assert cart_service.calculate_cart_totals(Cart()) == {
            "subtotal": 0.0, "gst": 0.0, "pst": 0.0, "service_charge": 0.0, "total": 0.0,
        }

    def test_charges_are_5_7_and_10_percent_of_subtotal(self, cart_service):
        from app.schemas.cart import Cart, CartItem

        cart = Cart(items=[CartItem(item_id=2, restaurant_id=1, quantity=1)])  # 12.50

        assert cart_service.calculate_cart_totals(cart) == {
            "subtotal": 12.50, "gst": 0.63, "pst": 0.88, "service_charge": 1.25, "total": 15.26,
        }

    def test_unknown_menu_item_raises(self, cart_service):
        from app.schemas.cart import Cart, CartItem

        cart = Cart(items=[CartItem(item_id=999, restaurant_id=1, quantity=1)])

        with pytest.raises(ValueError, match="not found"):
            cart_service.calculate_cart_totals(cart)

# class TestRemoveFromCart:
 
# class TestClearCart:
