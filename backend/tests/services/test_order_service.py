import pytest
from unittest.mock import MagicMock
from types import SimpleNamespace

from app.services.order_service import OrderService


@pytest.fixture
def user():
    return {
        "id": 1,
        "role": "customer",
        "firstname": "Brady",
        "lastname": "Bracken",
        "email": "brady@example.com",
        "phone": "2508638425",
        "address": {
            "street": "613 Clifton Court",
            "city": "Kelowna",
            "province": "BC",
            "postalcode": "V1V0B7",
        },
        "is_active": True,
        "cart": {
            "items": [
                {"item_id": 1, "restaurant_id": 1, "quantity": 2},
                {"item_id": 2, "restaurant_id": 1, "quantity": 1},
            ]
        },
    }


@pytest.fixture
def restaurant():
    return {
        "id": 1,
        "name": "A&W",
        "menu": [
            {
                "id": 1,
                "name": "Teen Burger",
                "price": 8.49,
                "availability": True,
                "active": True,
            },
            {
                "id": 2,
                "name": "Papa Burger",
                "price": 9.79,
                "availability": True,
                "active": True,
            },
        ],
    }


@pytest.fixture
def cart():
    return SimpleNamespace(
        items=[
            SimpleNamespace(
                item_id=1,
                restaurant_id=1,
                quantity=2,
            ),
            SimpleNamespace(
                item_id=2,
                restaurant_id=1,
                quantity=1,
            ),
        ]
    )


@pytest.fixture
def service(user, restaurant, cart):
    user_repo = MagicMock()
    user_repo.get_user_by_id.return_value = user

    restaurant_repo = MagicMock()
    restaurant_repo.get_restaurant_by_id.return_value = restaurant

    order_repo = MagicMock()

    # Simulate the repository assigning an ID and saving the order.
    def create_order_side_effect(order):
        order["id"] = 1
        return order

    order_repo.create_order.side_effect = create_order_side_effect

    cart_service = MagicMock()
    cart_service.get_cart.return_value = cart

    return OrderService(
        user_repository=user_repo,
        restaurant_repository=restaurant_repo,
        order_repository=order_repo,
        cart_service=cart_service,
    )


class TestCheckout:
    def test_checkout_creates_order(self, service):
        order = service.checkout(1)

        assert order["id"] == 1
        assert order["customer_id"] == 1
        assert order["restaurant_id"] == 1
        assert order["status"] == "pending"


    def test_checkout_calculates_correct_total(self, service):
        order = service.checkout(1)

        # 2 x $8.49 + 1 x $9.79
        assert order["total_price"] == 26.77


    def test_checkout_saves_item_snapshots(self, service):
        order = service.checkout(1)

        assert order["items"] == [
            {
                "item_id": 1,
                "name": "Teen Burger",
                "price": 8.49,
                "quantity": 2,
            },
            {
                "item_id": 2,
                "name": "Papa Burger",
                "price": 9.79,
                "quantity": 1,
            },
        ]


    def test_checkout_includes_customer_details(self, service):
        order = service.checkout(1)

        assert order["customer_details"]["firstname"] == "Brady"
        assert order["customer_details"]["lastname"] == "Bracken"
        assert order["customer_details"]["email"] == "brady@example.com"
        assert order["customer_details"]["address"]["city"] == "Kelowna"


    def test_checkout_sets_pending_status(self, service):
        order = service.checkout(1)

        assert order["status"] == "pending"


    def test_checkout_sets_created_at(self, service):
        order = service.checkout(1)

        assert "created_at" in order
        assert order["created_at"] is not None


    def test_checkout_no_cart(self, service):
        service.user_repository.get_user_by_id.return_value["cart"] = None

        with pytest.raises(ValueError, match="has no cart"):
            service.checkout(1)


    def test_checkout_empty_cart(self, service):
        service.cart_service.get_cart.return_value.items = []

        with pytest.raises(ValueError, match="empty cart"):
            service.checkout(1)


    def test_checkout_uses_current_menu_prices(self, service):
        restaurant = service.restaurant_repository.get_restaurant_by_id.return_value

        # Simulate the price changing after the item was added to the cart.
        restaurant["menu"][0]["price"] = 10.00

        order = service.checkout(1)

        # 2 x $10.00 + 1 x $9.79
        assert order["total_price"] == 29.79

        assert order["items"][0]["price"] == 10.00


class TestCustomerErrors:
    def test_checkout_customer_not_found(self, service):
        service.user_repository.get_user_by_id.return_value = None

        with pytest.raises(ValueError, match="does not exist"):
            service.checkout(999)


    def test_checkout_inactive_customer(self, service):
        service.user_repository.get_user_by_id.return_value["is_active"] = False

        with pytest.raises(ValueError, match="is not active"):
            service.checkout(1)

class TestMenuItemErrors:
    def test_checkout_menu_item_not_found(self, service):
        restaurant = service.restaurant_repository.get_restaurant_by_id.return_value

        restaurant["menu"] = [
            item for item in restaurant["menu"]
            if item["id"] != 2
        ]

        with pytest.raises(ValueError, match="not found in restaurant"):
            service.checkout(1)


    def test_checkout_unavailable_menu_item(self, service):
        restaurant = service.restaurant_repository.get_restaurant_by_id.return_value

        restaurant["menu"][0]["availability"] = False

        with pytest.raises(ValueError, match="currently unavailable"):
            service.checkout(1)


class TestPersistence:
    def test_checkout_persists_order(self, service):
        service.checkout(1)

        service.order_repository.create_order.assert_called_once()


    def test_checkout_clears_cart_after_successful_order(self, service):
        service.checkout(1)

        service.cart_service.clear_cart.assert_called_once_with(1)


    def test_checkout_saves_order_before_clearing_cart(self, service):
        events = []

        service.order_repository.create_order.side_effect = lambda order: (
            events.append("save_order"),
            order.update({"id": 1}),
            order
        )[-1]

        service.cart_service.clear_cart.side_effect = lambda user_id: (
            events.append("clear_cart")
        )

        service.checkout(1)

        assert events == ["save_order", "clear_cart"]


    def test_checkout_does_not_clear_cart_if_order_save_fails(self, service):
        service.order_repository.create_order.side_effect = OSError(
            "Failed to save order"
        )

        with pytest.raises(OSError, match="Failed to save order"):
            service.checkout(1)

        service.cart_service.clear_cart.assert_not_called()