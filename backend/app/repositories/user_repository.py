import json
import os


class UserRepository:
    def __init__(self, file_path: str = "data/users.json"):
        self.filePath = file_path  

    def get_all_users(self):
        try:
            with open(self.filePath, "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError: 
            raise FileNotFoundError(f"File not found: {self.filePath}")
        except json.JSONDecodeError:
            raise ValueError(f"Error is not valid JSON: {self.filePath}")

    def save_users(self, users):  
        temp_path = f"{self.filePath}.tmp"  
        try:  
            with open(temp_path, "w") as file:  
                json.dump(users, file, indent=4)  
            os.replace(temp_path, self.filePath)  
        except (OSError, TypeError, ValueError) as e:  
            raise OSError(f"Error saving data to {self.filePath}: {e}")

    def get_user_by_id(self, user_id: int):
        users = self.get_all_users()
        for user in users:
            if user.get("id") == user_id:
                return user
        return None

    def update_user(self, user_id: int, update_data: dict):
            users = self.get_all_users()
            
            for user in users:
                if user.get("id") == user_id:
                    user.update(update_data)
                    from datetime import UTC, datetime
                    user["last_modified"] = datetime.now(UTC).isoformat()
                    self.save_users(users)
                    return user
            return None