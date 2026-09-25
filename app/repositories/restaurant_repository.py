import json

class RestaurantRepository:
    def __init__(self, file_path: str = "data/restaurants.json"):
        self.filePath = file_path  

    def getAllRestaurants(self):
        try:
            with open(self.filePath, "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.filePath}")
        except json.JSONDecodeError:
            raise ValueError(f"Error is not valid JSON: {self.filePath}")
