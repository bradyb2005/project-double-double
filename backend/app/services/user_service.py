
from datetime import UTC, datetime

from app.core.security import get_password_hash
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def get_all_users(self):
        return self.user_repository.get_all_users()

    def create_user(self, user: UserCreate):
        users = self.user_repository.get_all_users()

        user_dict = user.model_dump()
        raw_password = user_dict.pop("password")
        
        user_dict["password_hash"] = get_password_hash(raw_password)
        
        new_id = max((u.get("id", 0) for u in users), default=0) + 1
        user_dict["id"] = new_id
        user_dict["created_at"] = datetime.now(UTC).isoformat()
        user_dict["last_updated"] = datetime.now(UTC).isoformat()
        
        users.append(user_dict)
        self.user_repository.save_users(users)
        
        return user_dict

    def update_user(self, user_id: int, update_data: UserUpdate) -> dict:
        update_dict = update_data.model_dump(exclude_unset=True)
        updated_user = self.user_repository.update_user(user_id, update_dict)
        if updated_user is None:
            raise ValueError("User not found")
        return updated_user

    def deactivate_user(self, user_id: int) -> dict:
        user = self.user_repository.get_user_by_id(user_id)
        
        if user is None:
            raise ValueError("User not found")
        if user.get("is_active") is False:
            raise ValueError("User is already deactivated")
        
        return self.user_repository.update_user(user_id, {"is_active": False})

    def view_user(self, user_id: int):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user