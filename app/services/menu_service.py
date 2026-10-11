from app.repositories.menu_repository import MenuRepository

class MenuService:
    def __init__(self) -> None:
        self.repository = MenuRepository()
        
    def fetch_restaurant_menu(self, restaurant_id: int):
        menu = self.repository.get_menu_by_restaurant_id(restaurant_id)
        if not menu:
            raise ValueError("Restaurants menu is empty")
        return menu