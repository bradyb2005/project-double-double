import pytest
from app.schemas.menu_item import ItemUpdate

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


def test_update_menu_item_second_item_actually_changes(restaurant_service):
    restaurant_service.update_menu_item(1, 2, ItemUpdate(price=1.23))
    menu = restaurant_service.fetch_restaurant_menu(1)
    assert menu[0]["price"] != 1.23
    assert menu[1]["price"] == 1.23

def test_update_menu_item_works_on_non_first_restaurant(restaurant_service, valid_menu_item_create):
    created = restaurant_service.create_menu_item(2, valid_menu_item_create)
    updated = restaurant_service.update_menu_item(2, created["id"], ItemUpdate(price=5.55))
    assert updated["price"] == 5.55

def test_update_menu_item_without_category_does_not_crash(restaurant_service):
    restaurant_service.update_menu_item(1, 1, ItemUpdate(price=9.99))
    menu = restaurant_service.fetch_restaurant_menu(1)
    assert menu[0]["price"] == 9.99
    assert menu[0]["category"]

def test_update_menu_item_unknown_item_raises(restaurant_service):
    with pytest.raises(ValueError, match="Menu item not found"):
        restaurant_service.update_menu_item(1, 9999, ItemUpdate(price=1.0))

def test_update_menu_item_unknown_restaurant_raises(restaurant_service):
    with pytest.raises(ValueError, match="Restaurant not found"):
        restaurant_service.update_menu_item(9999, 1, ItemUpdate(price=1.0))

def test_new_restaurant_can_receive_menu_item(restaurant_service, valid_restaurant_create, valid_menu_item_create):
    new = restaurant_service.create_restaurant(valid_restaurant_create)
    assert new["menu"] == []
    item = restaurant_service.create_menu_item(new["id"], valid_menu_item_create)
    assert item["id"] == 1