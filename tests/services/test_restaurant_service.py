import pytest
from app.schemas.restaurant import RestaurantUpdate

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

def test_update_restaurant_correct(restaurant_service): #test updating a restaurant with valid data.
    updated_restaurant = RestaurantUpdate(name="NewRestaurantName", address="123 st", postalcode="V1V1V1", phone="123-456-7890", location={"city": "NewCity", "province": "NewProvince"})
    
    result = restaurant_service.update_restaurant(1, updated_restaurant)
    
    assert result["name"] == "NewRestaurantName"
    assert result["address"] == "123 st"
    assert result["postalcode"] == "V1V1V1"
    assert result["phone"] == "123-456-7890"
    assert result["location"]["city"] == "NewCity"
    assert result["location"]["province"] == "NewProvince"

def test_update_restaurant_missing(restaurant_service): #test updating a restaurant with missing data.
    updated_restaurant = RestaurantUpdate(name="", address="   ") #spaces and empty
    
    result = restaurant_service.update_restaurant(1, updated_restaurant)
    
    assert result["name"] == "Test Restaurant 1"
    assert result["address"] == "123 Test St"

def test_update_restaurant_invalid_phone(restaurant_service): #test updating a restaurant with invalid phone number.
    updated_restaurant = RestaurantUpdate(phone="ThisIsNotValid")  # Invalid phone format
    
    with pytest.raises(ValueError) as excinfo:
        restaurant_service.update_restaurant(1, updated_restaurant)
    assert "Invalid phone number format. Must be ###-###-#### or ##########" in str(excinfo.value)

def test_update_restaurant_invalid_postalcode(restaurant_service): #test updating a restaurant with invalid postal code.
    updated_restaurant = RestaurantUpdate(postalcode="123456")  # Invalid postal code format
    
    with pytest.raises(ValueError) as excinfo:
        restaurant_service.update_restaurant(1, updated_restaurant)
    assert "Invalid postal code format. Must alternate letter and number" in str(excinfo.value)

def test_update_restaurant_missing_id(restaurant_service): #searching for a restaurant that does not exist.
    updated_restaurant = RestaurantUpdate(name="MissingRestaurant")  #
    
    result = restaurant_service.update_restaurant(1, updated_restaurant)
    
    with pytest.raises(ValueError) as excinfo:
        restaurant_service.update_restaurant(65769, updated_restaurant)
    assert "Restaurant of ID 65769 not found" in str(excinfo.value)

