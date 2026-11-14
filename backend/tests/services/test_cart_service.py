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


class TestAddToCart:
    def test_add_to_cart_adds_item(self, cart_service):
        updated_cart = cart_service.add_to_cart(1, item_id=1, restaurant_id=1, quantity=1)

        assert any(item.item_id == 1 for item in updated_cart.items)
        assert updated_cart.total == 5.99

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

    def test_add_to_cart_duplicate_item_updates_quantity(self, cart_service):
        cart_service.add_to_cart(1, item_id=1, restaurant_id=1, quantity=1)
        updated_cart = cart_service.add_to_cart(1, item_id=1, restaurant_id=1, quantity=2)

        assert [item.quantity for item in updated_cart.items if item.item_id == 1] == [1, 2]

# class TestRemoveFromCart:
 
# class TestUpdateCart:

# class TestClearCart:

# class TestCalculateCartTotal: