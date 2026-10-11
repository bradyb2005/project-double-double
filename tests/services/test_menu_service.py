import pytest
import json

def test_fetch_menu_with_known_id(menu_service):
    menu = menu_service.fetch_restaurant_menu(1)
    assert isinstance(menu, list)
    assert menu[0]['id'] == 1
    
def test_fetch_menu_with_invalid_id(menu_service):
    with pytest.raises(ValueError, match="Restaurants menu is empty"):
        menu_service.fetch_restaurant_menu(99999)