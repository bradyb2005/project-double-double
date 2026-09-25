import pytest
from app.repositories.restaurant_repository import RestaurantRepository

def test_get_all_restaurants_returns_list():
    repo = RestaurantRepository()
    result = repo.get_all_restaurants()
    assert isinstance(result, list)

def test_missing_file_raises_error():
    repo = RestaurantRepository(file_path="non_existent_file.json")
    with pytest.raises(FileNotFoundError):
        repo.get_all_restaurants()

def test_invalid_json_raises_error(tmp_path):
    bad_file = tmp_path / "bad_file.json"
    bad_file.write_text("Not valid JSON")
    repo = RestaurantRepository(str(bad_file))
    with pytest.raises(ValueError):
        repo.get_all_restaurants()