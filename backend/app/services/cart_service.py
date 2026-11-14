from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.user_repository import UserRepository
from app.schemas.cart import Cart, CartItem


class CartService:
    def __init__(self, user_repository: UserRepository | None = None):
        self.user_repository = user_repository or UserRepository()

    def calculate_cart_total(self, cart: Cart) -> float:
        total = 0.0
        if cart.items:
            restaurant_id = cart.items[0].restaurant_id
            restaurant_repo = RestaurantRepository()
            restaurant = restaurant_repo.get_restaurant_by_id(restaurant_id)
        else:
            return 0.0
        for item in cart.items:
            if restaurant is None:
                raise ValueError("Restaurant not found")
            menu_item = next((i for i in restaurant.get("menu", []) if i["id"] == item.item_id), None)
            if menu_item is None:
                raise ValueError(f"Menu item with ID {item.item_id} not found in restaurant {restaurant_id}")
            total += menu_item["price"] * item.quantity
        return total

    def get_cart(self, user_id: int) -> Cart:
        user = self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise ValueError("User not found")

        return Cart.model_validate(user.get("cart") or {})

    def add_to_cart(self, user_id: int, item_id: int, restaurant_id: int, quantity: int) -> Cart:
        cart = self.get_cart(user_id)

        if cart.items and any(item.restaurant_id != restaurant_id for item in cart.items):
            raise ValueError("Cannot add items from different restaurants to the cart")

        item = CartItem(item_id=item_id, restaurant_id=restaurant_id, quantity=quantity)
        cart.items.append(item)
        cart.total = self.calculate_cart_total(cart)
        if self.user_repository.update_cart(user_id, cart.model_dump(mode="json")) is None:
            raise ValueError("User not found")
        return cart

    def remove_from_cart(self, user_id: int, item_id: int) -> Cart:
        cart = self.get_cart(user_id)
        cart.items = [item for item in cart.items if item.item_id != item_id]
        cart.total = self.calculate_cart_total(cart)
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

        cart.total = self.calculate_cart_total(cart)
        if self.user_repository.update_cart(user_id, cart.model_dump(mode="json")) is None:
            raise ValueError("User not found")
        return cart

    def clear_cart(self, user_id: int) -> Cart:
        cart = self.get_cart(user_id)
        cart.items = []
        cart.total = 0.0
        if self.user_repository.update_cart(user_id, cart.model_dump(mode="json")) is None:
            raise ValueError("User not found")
        return cart