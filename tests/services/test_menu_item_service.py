import pytest

def test_create_menu_item(restaurant_service, valid_menu_item_create):
   result = restaurant_service.create_menu_item(1, valid_menu_item_create)
   assert result["name"] == valid_menu_item_create.name
   assert result["price"] == valid_menu_item_create.price
   assert result["category"] == valid_menu_item_create.category

def test_create_menu_item_invalid_price(restaurant_service, valid_menu_item_create):
    valid_menu_item_create.price = -1.0

    with pytest.raises(ValueError) as excinfo:
        restaurant_service.create_menu_item(1, valid_menu_item_create)
    assert "greater than 0" in str(excinfo.value) 