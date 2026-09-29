import re
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.restaurant import RestaurantCreate


class RestaurantService:
    def __init__(self):
        self.repository = RestaurantRepository()

    def fetch_restaurant_list(self):
        return self.repository.get_all_restaurants()

    def validate_restaurant_data(self, data: RestaurantCreate) -> None:
        # 1. Non-optional attributes not empty[cite: 2]
        required_strings = [
            data.name,
            data.cuisine,
            data.phone,
            data.address,
            data.postalcode,
            data.location.city,
            data.location.province,
        ]
        if any(not s or not str(s).strip() for s in required_strings):
            raise ValueError("Non-optional fields cannot be empty")

        # The below regex just means the phone number be ###-###-#### or ##########.
        phone_pattern = r"^(\d{3}-\d{3}-\d{4}|\d{10})$"
        if not data.phone or not re.match(phone_pattern, data.phone.strip()):
            raise ValueError("Invalid phone number format. Must be ###-###-#### or ##########")

        cleaned_postal = data.postalcode.replace(" ", "").upper()
        postal_pattern = r"^[A-Z]\d[A-Z]\d[A-Z]\d$"
        if not re.match(postal_pattern, cleaned_postal):
            raise ValueError("Invalid postal code format. Must alternate letter and number")

        data.postalcode = cleaned_postal

    def create_restaurant(self, restaurant: RestaurantCreate):
        self.validate_restaurant_data(restaurant)
        restaurants = self.repository.get_all_restaurants()

        restaurant_dict = restaurant.model_dump()
        new_id = max((r.get("id", 0) for r in restaurants), default=0) + 1
        restaurant_dict = {"id": new_id, **restaurant_dict}

        restaurants.append(restaurant_dict)
        self.repository.save_restaurants(restaurants)

        return restaurant_dict