import pytest

def test_create_restaurant_success(restaurant_service, valid_restaurant_create):
    result = restaurant_service.create_restaurant(valid_restaurant_create)
    assert result["name"] == valid_restaurant_create.name
    assert result["address"] == valid_restaurant_create.address
    assert result["postalcode"] == valid_restaurant_create.postalcode
    assert result["phone"] == valid_restaurant_create.phone
    assert result["location"]["city"] == valid_restaurant_create.location.city
    assert result["location"]["province"] == valid_restaurant_create.location.province

def test_create_restaurant_missing_required_field(restaurant_service, valid_restaurant_create):
    valid_restaurant_create.name = ""
    with pytest.raises(ValueError) as excinfo:
        restaurant_service.create_restaurant(valid_restaurant_create)
    assert "Non-optional fields cannot be empty" in str(excinfo.value)

