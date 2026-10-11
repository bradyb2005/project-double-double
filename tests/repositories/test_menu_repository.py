import pytest
from app.repositories.menu_repository import MenuRepository

def test_missing_file_raises_error():
    repo = MenuRepository(file_path="non_existent_file.json")
    with pytest.raises(FileNotFoundError):
        repo.get_all_menu_items()

# Extra test - Checking for invalid JSON content
def test_invalid_json_raises_error(tmp_path):
    bad_file = tmp_path / "bad_file.json"
    bad_file.write_text("Not valid JSON")
    repo = MenuRepository(str(bad_file))
    with pytest.raises(ValueError):
        repo.get_all_menu_items()
        

def test_get_menu_by_restaurant_returns_list():
    repo = MenuRepository()
    result = repo.get_menu_by_restaurant_id(1)
    assert isinstance(result, list)
