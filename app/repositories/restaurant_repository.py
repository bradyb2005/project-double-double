import json
import os

class RestaurantRepository:
    def __init__(self, file_path: str = "data/restaurants.json"):
        self.filePath = file_path  

    def get_all_restaurants(self):
        try:
            with open(self.filePath, "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError: 
            raise FileNotFoundError(f"File not found: {self.filePath}")
        except json.JSONDecodeError:
            raise ValueError(f"Error is not valid JSON: {self.filePath}")

    def save_restaurants(self, restaurants):  
        temp_path = f"{self.filePath}.tmp"  
        try:  
            with open(temp_path, "w") as file:  
                json.dump(restaurants, file, indent=4)  
            os.replace(temp_path, self.filePath)  
        except Exception as e:  
            raise IOError(f"Error saving data to {self.filePath}: {e}")

    def get_all_restaurant_names(self):
        restaurants = self.get_all_restaurants()
        return [restaurant['name'] for restaurant in restaurants]
    