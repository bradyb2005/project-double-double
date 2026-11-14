import pytest


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

class TestGetCart:
    def test_get_cart_returns_existing_cart(self, user_repository):
        from app.services.cart_service import CartService

        cart = CartService(user_repository).get_cart(1)

        assert cart.items == []
        assert cart.total == 0.0

    def test_get_cart_invalid_user_raises(self, user_repository):
        from app.services.cart_service import CartService

        with pytest.raises(ValueError, match="User not found"):
            CartService(user_repository).get_cart(999)


# class TestAddToCart:
    
# class TestRemoveFromCart:
 
# class TestUpdateCart:

# class TestClearCart:

# class TestCalculateCartTotal: