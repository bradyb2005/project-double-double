import json

class RestaurantRepository:
    def __init__(self):
        self.filePath = "data/restaurants.json"

    def get_all_restaurants(self):
        file = open(self.filePath, "r")
        data = json.load(file)
        file.close()
        return data