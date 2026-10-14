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

def test_create_restaurant_invalid_phone(restaurant_service, valid_restaurant_create):
    valid_restaurant_create.phone = "1250-123-4567"  # Invalid phone format (extra number at the start)
    with pytest.raises(ValueError) as excinfo:
        restaurant_service.create_restaurant(valid_restaurant_create)
    assert "Invalid phone number format" in str(excinfo.value)

def test_create_restaurant_invalid_postalcode(restaurant_service, valid_restaurant_create):
    valid_restaurant_create.postalcode = "123456"  # Invalid postal code format (does not alternate letter/number)
    with pytest.raises(ValueError) as excinfo:
        restaurant_service.create_restaurant(valid_restaurant_create)
    assert "Invalid postal code format" in str(excinfo.value)

def test_fetch_all_restaurant_names(restaurant_service):
    names = restaurant_service.fetch_all_restaurant_names()
    assert names == ["Test Restaurant 1", "Test Restaurant 2"]