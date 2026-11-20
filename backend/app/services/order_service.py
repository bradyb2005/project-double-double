from app.repositories.user_repository import UserRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.order_repository import OrderRepository
from app.services.cart_service import CartService


from datetime import UTC, datetime
from decimal import Decimal, ROUND_HALF_UP


CENT = Decimal("0.01")


def money(value):
    return Decimal(str(value)).quantize(
        CENT,
        rounding=ROUND_HALF_UP
    )




class OrderService:
    def __init__(
        self,
        user_repository = None,
        restaurant_repository = None,
        order_repository = None,
        cart_service = None,
    ):
        self.user_repository = user_repository or UserRepository()
        self.restaurant_repository = ( restaurant_repository or RestaurantRepository() )
        self.order_repository = order_repository or OrderRepository()
        self.cart_service = cart_service or CartService(
            self.user_repository
        )

    def checkout(self, user_id: int):
        # Validate customer: exists and is active
        user = self.user_repository.get_user_by_id(user_id)

        if user is None:
            raise ValueError(f"User with ID {user_id} does not exist.")

        if not user.get("is_active", True):
            raise ValueError(f"User with ID {user_id} is not active.")

        # Validate cart: exists, not empty, items from a single restaurant, items are all available,
        #   item quantities are valid, and calculate total price

        # Check cart exists:
        if not user.get("cart"):
            raise ValueError(f"User with ID {user_id} has no cart.")
        cart = self.cart_service.get_cart(user_id)
        #Check cart is not empty
        if not cart.items:
            raise ValueError(f"Cannot checkout empty cart for user with ID {user_id}.")

        # Validate that all items are from the same restaurant
        restaurant_ids = {
            item.restaurant_id for item in cart.items
        }
        if len(restaurant_ids) != 1:
            raise ValueError(f"Cart contains items from multiple restaurants for user with ID {user_id}.")\
            
        restaurant_id = next(iter(restaurant_ids))
        restaurant = self.restaurant_repository.get_restaurant_by_id(
            restaurant_id
        )

        if restaurant is None:
            raise ValueError("Restaurant not found")

        # Validate item quantitiy > 0, is_available = true, and item exists
        total = Decimal("0.00")
        order_items = []
        for cart_item in cart.items:
            menu_item = next(
                (item for item in restaurant.get("menu", [])
                    if item.get("id") == cart_item.item_id),
                None
            )

            if menu_item is None:
                raise ValueError(f"Item with ID {cart_item.item_id} not found in restaurant with ID {restaurant_id}.")
            if not menu_item.get("availability", True):
                raise ValueError(
                    f"Item with ID {cart_item.item_id} is currently unavailable."
                )
            if cart_item.quantity <= 0:
                raise ValueError(f"Invalid quantity for item with ID {cart_item.item_id}. Quantity must be greater than 0.")

            
            current_price = money(menu_item["price"])

            if not current_price.is_finite() or current_price < 0:
                raise ValueError(
                    f"Invalid price for {menu_item['name']}"
                )

            quantity = cart_item.quantity
            item_total = current_price * quantity

            total += item_total

            # Save item details for order creation
            order_items.append({
                "item_id": menu_item["id"],
                "name": menu_item["name"],
                "price": float(current_price),
                "quantity": quantity
            })

        # Save customer details for order creation
        customer_details = {
            "firstname": user.get("firstname"),
            "lastname": user.get("lastname"),
            "email": user.get("email"),
            "phone": user.get("phone"),
            "address": user.get("address")
        }

        # Create order data
        order = {
            "customer_id": user_id,
            "customer_details": customer_details,
            "restaurant_id": restaurant_id,
            "items": order_items,
            "total_price": float(money(total)),
            "status": "pending",
            "created_at": datetime.now(UTC).isoformat()
        }

        # Save the order
        created_order = self.order_repository.create_order(order)


        # Clear the cart
        if created_order:
            self.cart_service.clear_cart(user_id)

        return created_order

    def get_customer_orders(self, user_id: int):
        orders = self.order_repository.get_orders_by_customer_id(user_id)
        return sorted(
            orders,
            key=lambda order: (order.get("created_at", ""), order.get("id", 0)),
            reverse=True,
        )

    def get_customer_order(self, user_id: int, order_id: int):
        order = self.order_repository.get_order_by_id(order_id)
        if order is None or order.get("customer_id") != user_id:
            raise ValueError(f"Order with ID {order_id} not found.")
        return order
