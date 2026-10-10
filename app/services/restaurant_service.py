import re
from app.repositories.restaurant_repository import RestaurantRepository
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

    def update_restaurant(self,restaurant_id: int, restaurant: RestaurantUpdate):
        self.validate_phone_postal(restaurant) #validate phonee and postal code if changed 
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