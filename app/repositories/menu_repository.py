import json

class MenuRepository:
    def __init__(self, file_path: str = "data/menus.json"):
        self.file_path = file_path
        
    def get_all_menu_items(self) -> list[dict]:
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.file_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Error is not valid JSON: {self.file_path}")
        
    def get_menu_by_restaurant_id(self, restaurant_id: int) -> list[dict]:
        menu = self.get_all_menu_items()
        res = []
        
        for item in menu:
            if item['restaurant_id'] == restaurant_id:
                res.append(item)
                
        return res
