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

def test_update_menu_item(restaurant_service,valid_menu_item_create):
    created_item = restaurant_service.create_menu_item(1,valid_menu_item_create)

    item_id = created_item["id"]

    updated_item_data = valid_menu_item_create.model_copy(update={"name": "Updated Name","price": 15.99})

    updated_item = restaurant_service.update_menu_item(1,created_item["id"],updated_item_data)

    assert updated_item["name"] == "Updated Name"
    assert updated_item["price"] == 15.99

def test_update_menu_item_invalid_price(restaurant_service, valid_menu_item_create):
    created_item = restaurant_service.create_menu_item(1, valid_menu_item_create)

    updated_item_data = valid_menu_item_create.model_copy(update={"price": -1.0})

    with pytest.raises(ValueError) as excinfo:
        restaurant_service.update_menu_item(1, created_item["id"], updated_item_data)
    assert "greater than 0" in str(excinfo.value)