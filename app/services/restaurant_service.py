import re
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.restaurant import RestaurantCreate
from app.schemas.menu_item import ItemCreate

class RestaurantService:
    def __init__(self):
        self.repository = RestaurantRepository()

    def fetch_restaurant_list(self):
        return self.repository.get_all_restaurants()

    def fetch_all_restaurant_names(self):
        return self.repository.get_all_restaurant_names()

    def validate_restaurant_data(self, data: RestaurantCreate) -> None:
        # 1. Non-optional attributes not empty[cite: 2]
        required_strings = [
            data.name,
            data.address,
            data.postalcode,
            data.location.city,
            data.location.province,
        ]
        if any(not s or not str(s).strip() for s in required_strings):
            raise ValueError("Non-optional fields cannot be empty")

        # The below regex just means the phone number be ###-###-#### or ##########.
        phone_pattern = r"^(\d{3}-\d{3}-\d{4}|\d{10})$"
        if data.phone is not None and (
            not data.phone.strip() or not re.match(phone_pattern, data.phone.strip())
        ):
            raise ValueError("Invalid phone number format. Must be ###-###-#### or ##########")

        # Strip spaces and convert to uppercase for postal code validation
        cleaned_postal = data.postalcode.replace(" ", "").upper()
        # The below regex checks for the Canadian postal code format: letter-number-letter-number-letter-number.
        postal_pattern = r"^[A-Z]\d[A-Z]\d[A-Z]\d$"
        if not re.match(postal_pattern, cleaned_postal):
            raise ValueError("Invalid postal code format. Must alternate letter and number")

    def create_restaurant(self, restaurant: RestaurantCreate):
        self.validate_restaurant_data(restaurant)
        restaurants = self.repository.get_all_restaurants()

        restaurant_dict = restaurant.model_dump()
        new_id = max((r.get("id", 0) for r in restaurants), default=0) + 1
        restaurant_dict = {"id": new_id, **restaurant_dict}

        restaurants.append(restaurant_dict)
        self.repository.save_restaurants(restaurants)

        return restaurant_dict

    def create_menu_item(self, restaurant_id: int, item: ItemCreate):
        restaurant = self.repository.get_restaurant_by_id(restaurant_id)
        if restaurant is None:
            raise ValueError("Restaurant not found")
        
        self.validate_menu_item_data(item)

        item_dict = item.model_dump()

        menu = restaurant.get("menu", [])

        new_id = max((menu_item.get("id", 0) for menu_item in menu),default=0) + 1

        item_dict = {"id": new_id, **item_dict}

        return self.repository.add_menu_item(restaurant_id, item_dict)


    def validate_menu_item_data(self, item):
       allowed_categories = [
           "Starters",
            "Pizza",
            "Pasta",
            "Mains",
            "Vegetarian",
            "Dim Sum",
            "Rolls",
            "Nigiri",
            "Burgers",
            "Sides",
            "Bread",
            "Tacos",
            "Burritos",
            "Dessert",
            "Drinks",
       ]
       if not item.name.strip():
           raise ValueError("Item name cannot be empty")

       if item.price <= 0:
              raise ValueError("Item price must be greater than 0")

       if item.category.strip().lower() not in [item.lower() for item in allowed_categories]:
              raise ValueError("Invalid category")