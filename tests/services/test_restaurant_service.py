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
    assert names == ["Test Restaurant 1", "Test Restaurant 2", "Test Restaurant 3"]

# --- Search and Filter Tests ---

def test_search_and_filter_no_params_returns_all(restaurant_service, restaurant_filter):
    filters = restaurant_filter()
    results = restaurant_service.search_and_filter_restaurants(filters)
    assert len(results) == 3


def test_search_by_name_case_insensitive(restaurant_service, restaurant_filter):
    filters = restaurant_filter(search="restaurant 2")
    results = restaurant_service.search_and_filter_restaurants(filters)
    assert len(results) == 1
    assert results[0]["name"] == "Test Restaurant 2"


def test_search_by_cuisine_keyword(restaurant_service, restaurant_filter):
    filters = restaurant_filter(search="italian")
    results = restaurant_service.search_and_filter_restaurants(filters)
    assert len(results) == 2
    assert all("italian" in r["cuisine"].lower() for r in results)


def test_filter_by_exact_cuisine(restaurant_service, restaurant_filter):
    filters = restaurant_filter(cuisine="Mexican")
    results = restaurant_service.search_and_filter_restaurants(filters)
    assert len(results) == 1
    assert results[0]["name"] == "Test Restaurant 2"


def test_filter_by_city(restaurant_service, restaurant_filter):
    filters = restaurant_filter(city="Another City")
    results = restaurant_service.search_and_filter_restaurants(filters)
    assert len(results) == 1
    assert results[0]["name"] == "Test Restaurant 2"


def test_filter_by_province(restaurant_service, restaurant_filter):
    filters = restaurant_filter(province="Another Province")
    results = restaurant_service.search_and_filter_restaurants(filters)
    assert len(results) == 2
    assert all(r["location"]["province"] == "Another Province" for r in results)


def test_filter_by_rating(restaurant_service, restaurant_filter):
    filters = restaurant_filter(rating=4.0)
    results = restaurant_service.search_and_filter_restaurants(filters)
    assert len(results) == 2
    assert all(r["rating"] >= 4.0 for r in results)


def test_filter_multi_combination(restaurant_service, restaurant_filter):
    filters = restaurant_filter(cuisine="Italian", province="Another Province", rating=3.0)
    results = restaurant_service.search_and_filter_restaurants(filters)
    assert len(results) == 1
    assert results[0]["name"] == "Test Restaurant 3"


def test_filter_no_results(restaurant_service, restaurant_filter):
    filters = restaurant_filter(search="NonExistentPlace")
    results = restaurant_service.search_and_filter_restaurants(filters)
    assert len(results) == 0