from app.repositories.user_repository import UserRepository
from app.schemas.cart import Cart, CartItem
from app.schemas.user import User, UserBase, UserCreate, UserUpdate


class CartService:
    def __init__(self):
        self.user_repository = UserRepository()

    def calculate_cart_total(self, cart: Cart) -> float:
        return 0.0
    
    def get_cart(self, user_id: int) -> Cart:
        return Cart()
    
    def add_to_cart(self, user_id: int, item_id: int, restaurant_id: int, quantity: int) -> Cart:
        return Cart()

    def remove_from_cart(self, user_id: int, item_id: int) -> Cart:
        return Cart()

    def update_cart_item(self, user_id: int, item_id: int, quantity: int) -> Cart:
        return Cart()

    def clear_cart(self, user_id: int) -> Cart:
        return Cart()