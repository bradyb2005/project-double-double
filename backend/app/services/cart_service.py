from app.repositories.user_repository import UserRepository
from app.schemas.cart import Cart, CartItem


class CartService:
    def __init__(self):
        self.user_repository = UserRepository()

    def calculate_cart_total(self, cart: Cart) -> float:
        return 0.0
    
    def get_cart(self, user_id: int) -> Cart:
        user = self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise ValueError("User not found")
        
        cart_data = user.get("cart", {})
        cart = Cart.model_validate(cart_data)
        return cart
    
    def add_to_cart(self, user_id: int, item_id: int, restaurant_id: int, quantity: int) -> Cart:
        user = self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise ValueError("User not found")
        
        current_rest_id = user.get("cart", {}).get("restaurant_id")
        if current_rest_id is not None and current_rest_id != restaurant_id:
            raise ValueError("Cannot add items from different restaurants to the cart")

        item = CartItem(item_id=item_id, restaurant_id=restaurant_id, quantity=quantity)
        cart_data = user.get("cart", {})
        cart = Cart.model_validate(cart_data)
        cart.items.append(item)
        
        cart.total = self.calculate_cart_total(cart)
        return cart

    def remove_from_cart(self, user_id: int, item_id: int) -> Cart:
        user = self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise ValueError("User not found")
        
        cart_data = user.get("cart", {})
        cart = Cart.model_validate(cart_data)
        cart.items = [item for item in cart.items if item.item_id != item_id]
        
        cart.total = self.calculate_cart_total(cart)
        return cart

    def update_cart_item(self, user_id: int, item_id: int, new_quantity: int) -> Cart:
        user = self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise ValueError("User not found")
        
        cart_data = user.get("cart", {})
        cart = Cart.model_validate(cart_data)
        
        for item in cart.items:
            if item.item_id == item_id:
                item.quantity = new_quantity
                break
        else:
            raise ValueError("Item not found in cart")
        
        cart.total = self.calculate_cart_total(cart)
        return cart

    def clear_cart(self, user_id: int) -> Cart:
        user = self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise ValueError("User not found")
        
        cart = Cart(items=[], total=0.0)
        return cart