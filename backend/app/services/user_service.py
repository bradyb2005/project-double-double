
from datetime import datetime, timezone

from backend.app.core.security import get_password_hash
from backend.app.schemas.user import UserCreate, UserUpdate


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
        now = datetime.now(timezone.utc).isoformat()
        
        user_dict["id"] = new_id
        user_dict["created_at"] = now
        user_dict["last_modified"] = now
        
        users.append(user_dict)
        self.user_repository.save_users(users)
        
        return user_dict

    def update_user(self, user_id: int, update_data: UserUpdate):
        updated_user = self.user_repository.update_user(user_id, update_data)
        if updated_user is None:
            raise ValueError("User not found")
        return updated_user

    def deactivate_user(self, user_id: int):
        updated_user = self.user_repository.get_user_by_id(user_id)
        if updated_user is None:
            raise ValueError("User not found")
        if updated_user.get("is_active", False):
            raise ValueError("User is already deactivated")
        
        updated_user["is_active"] = False
        updated_user["last_modified"] = datetime.now(timezone.utc).isoformat()
        self.user_repository.save_users(self.user_repository.get_all_users())

        return updated_user