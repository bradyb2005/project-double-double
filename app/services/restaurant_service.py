import re
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.restaurant import RestaurantCreate
from app.schemas.menu_item import ItemCreate
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


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

    def validate_phone_postal(self, data: RestaurantUpdate) -> None:
        # The below regex just means the phone number be ###-###-#### or ##########.
        phone_pattern = r"^(\d{3}-\d{3}-\d{4}|\d{10})$"
        if data.phone is not None and (
            not data.phone.strip() or not re.match(phone_pattern, data.phone.strip())
        ):
            raise ValueError("Invalid phone number format. Must be ###-###-#### or ##########")

        # Strip spaces and convert to uppercase for postal code validation
        if data.postalcode is not None:
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
       if item.name is not None:
           if not item.name.strip():
            raise ValueError("Item name cannot be empty")

       if item.price is not None and item.price <= 0:
              raise ValueError("Item price must be greater than 0")

       if item.category.strip().lower() not in [item.lower() for item in allowed_categories]:
              raise ValueError("Invalid category")

    def update_restaurant(self,restaurant_id: int, restaurant: RestaurantUpdate):
        self.validate_phone_postal(restaurant) #validate phone and postal code if changed
        restaurants = self.repository.get_all_restaurants()

        restaurant_dict = restaurant.model_dump(exclude_unset=True) #ignore missing fields

        update_data = {}
        for i, value in restaurant_dict.items():
            if isinstance(value, str) and not value.strip():
                continue

            update_data[i] = value


        #find the index by id
        for index, existing_restaurant in enumerate(restaurants):
            if existing_restaurant.get("id") == restaurant_id:
                
                #merge
                updated_restaurant = {**existing_restaurant, **update_data}
                
                restaurants[index] = updated_restaurant
                self.repository.save_restaurants(restaurants)
                return updated_restaurant
        #if not found by id
        raise ValueError(f"Restaurant of ID {restaurant_id} not found")

    def update_menu_item(self,restaurant_id: int,item_id: int,item: ItemCreate):
        self.validate_menu_item_data(item)

        restaurants = self.repository.get_all_restaurants()

        for restaurant in restaurants:
             if restaurant["id"] == restaurant_id:

                item_dict = item.model_dump(exclude_unset=True)
                item_dict["id"] = item_id

                for index, menu_item in enumerate(restaurant["menu"]):
                    if menu_item["id"] == item_id:

                        restaurant["menu"][index].update(item_dict)

                        self.repository.save_restaurants(restaurants)

                    return item_dict

                raise ValueError("Menu item not found")

             raise ValueError("Restaurant not found")
