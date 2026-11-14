from app.repositories.user_repository import UserRepository
from app.schemas.cart import Cart, CartItem
from app.schemas.user import User, UserBase, UserCreate, UserUpdate


class CartService:
    def __init__(self):
        self.user_repository = UserRepository()