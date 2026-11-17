from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.user_repository import UserRepository
from app.schemas.cart import Cart, CartItem
from decimal import ROUND_HALF_UP, Decimal

GST_RATE = Decimal("0.05")
PST_RATE = Decimal("0.07")  # BC only for now
SERVICE_CHARGE_RATE = Decimal("0.10")
CENT = Decimal("0.01")


def _money(value) -> Decimal:
    """Round to cents, half up."""
    return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)

class CartService:
    def __init__(self, user_repository: UserRepository | None = None):
        self.user_repository = user_repository or UserRepository()
        self.restaurant_repository = RestaurantRepository()

    def calculate_cart_subtotal(self, cart: Cart) -> float:
        total = Decimal("0.00")
        if cart.items:
            restaurant_id = cart.items[0].restaurant_id
            restaurant = self.restaurant_repository.get_restaurant_by_id(restaurant_id)
        else:
            return 0.0
        for item in cart.items:
            if restaurant is None:
                raise ValueError("Restaurant not found")
            menu_item = next((i for i in restaurant.get("menu", []) if i["id"] == item.item_id), None)
            if menu_item is None:
                raise ValueError(f"Menu item with ID {item.item_id} not found in restaurant {restaurant_id}")
            total += _money(menu_item["price"]) * item.quantity
        return float(total)

    def calculate_cart_totals(self, cart: Cart) -> dict[str, float]:
        subtotal = _money(self.calculate_cart_subtotal(cart))
        gst = _money(subtotal * GST_RATE)
        pst = _money(subtotal * PST_RATE)
        service_charge = _money(subtotal * SERVICE_CHARGE_RATE)
        total = subtotal + gst + pst + service_charge
        return {
            "subtotal": float(subtotal),
            "gst": float(gst),
            "pst": float(pst),
            "service_charge": float(service_charge),
            "total": float(total),
        }

    def get_available_menu_item(self, restaurant_id: int, item_id: int) -> dict:
        restaurant = self.restaurant_repository.get_restaurant_by_id(restaurant_id)
        if restaurant is None:
            raise ValueError("Restaurant not found")
        menu_item = next((i for i in restaurant.get("menu", []) if i["id"] == item_id), None)
        if menu_item is None:
            raise ValueError(f"Menu item with ID {item_id} not found in restaurant {restaurant_id}")
        if not menu_item.get("availability", True):
            raise ValueError(f"Menu item with ID {item_id} is not available")
        return menu_item

    def require_active_user(self, user_id: int) -> None:
        user = self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise ValueError("User not found")
        if not user.get("is_active", True):
            raise ValueError("Inactive customers cannot modify their cart")
          
    def apply_totals(self, cart: Cart) -> None:
        for field, value in self.calculate_cart_totals(cart).items():
            setattr(cart, field, value)

    def get_cart(self, user_id: int) -> Cart:
        user = self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise ValueError("User not found")

        cart = Cart.model_validate(user.get("cart") or {})
        items: dict[tuple[int, int], CartItem] = {}
        for item in cart.items:
            key = (item.restaurant_id, item.item_id)
            if key in items:
                items[key].quantity += item.quantity
            else:
                items[key] = item
        cart.items = list(items.values())
        return cart

    def add_to_cart(self, user_id: int, item_id: int, restaurant_id: int, quantity: int) -> Cart:
        self.require_active_user(user_id)
        cart = self.get_cart(user_id)

        if cart.items and any(item.restaurant_id != restaurant_id for item in cart.items):
            raise ValueError("Cannot add items from different restaurants to the cart")
        
        self.get_available_menu_item(restaurant_id, item_id)
        item = CartItem(item_id=item_id, restaurant_id=restaurant_id, quantity=quantity)
        existing_item = next((i for i in cart.items if i.item_id == item_id), None)
        if existing_item is not None:
            existing_item.quantity += item.quantity
        else:
            cart.items.append(item)
        self.apply_totals(cart)
        if self.user_repository.update_cart(user_id, cart.model_dump(mode="json")) is None:
            raise ValueError("User not found")
        return cart

    def remove_from_cart(self, user_id: int, item_id: int) -> Cart:
        cart = self.get_cart(user_id)
        cart.items = [item for item in cart.items if item.item_id != item_id]
        self.apply_totals(cart)
        if self.user_repository.update_cart(user_id, cart.model_dump(mode="json")) is None:
            raise ValueError("User not found")
        return cart

    def update_cart_item(self, user_id: int, item_id: int, new_quantity: int) -> Cart:
        cart = self.get_cart(user_id)

        for item in cart.items:
            if item.item_id == item_id:
                item.quantity = CartItem(
                    item_id=item.item_id,
                    restaurant_id=item.restaurant_id,
                    quantity=new_quantity,
                ).quantity
                break
        else:
            raise ValueError("Item not found in cart")

        self.apply_totals(cart)
        if self.user_repository.update_cart(user_id, cart.model_dump(mode="json")) is None:
            raise ValueError("User not found")
        return cart

    def clear_cart(self, user_id: int) -> Cart:
        cart = self.get_cart(user_id)
        cart.items = []
        self.apply_totals(cart)
        if self.user_repository.update_cart(user_id, cart.model_dump(mode="json")) is None:
            raise ValueError("User not found")
        return cart