from app.repositories.restaurant_repository import RestaurantRepository

class RestaurantService:
    def __init__(self):
        self.repository = RestaurantRepository()

    def fetch_restaurant_list(self):
        return self.repository.get_all_restaurants()

    def create_restaurant(self, restaurant: dict):
        restaurants = self.repository.get_all_restaurants()
        restaurants.append(restaurant)
        self.repository.save_restaurants(restaurants)
        return restaurant
