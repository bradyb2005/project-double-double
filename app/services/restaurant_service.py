from app.repositories.restaurant_repository import RestaurantRepository

class RestaurantService:
    def __init__(self):
        self.repository = RestaurantRepository()

    def fetchRestaurantList(self):
        return self.repository.getAllRestaurants()
