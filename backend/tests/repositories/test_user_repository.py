import pytest
from app.repositories.user_repository import UserRepository


class TestGetAllUsers:
    def test_get_all_users_returns_fixture_data(self, user_repository):
        users = user_repository.get_all_users()

        assert len(users) == 1
        assert users[0]["id"] == 1
        assert users[0]["email"] == "john.doe@example.com"

class TestSaveUsers:
    def test_save_users_persists_data(self, user_repository):
        users = [{"id": 2, "email": "new.user@example.com"}]

        user_repository.save_users(users)

        assert user_repository.get_all_users() == users

class TestGetUserById:
    def test_get_user_by_id_returns_matching_user(self, user_repository):
        user = user_repository.get_user_by_id(1)

        assert user is not None
        assert user["firstname"] == "John"

    def test_get_user_by_id_returns_none_for_unknown_user(self, user_repository):
        assert user_repository.get_user_by_id(999) is None

class TestUpdateUser:
    def test_update_user_updates_and_persists_user(self, user_repository):
        updated_user = user_repository.update_user(1, {"firstname": "Jane", "is_active": False})

        assert updated_user is not None
        assert updated_user["firstname"] == "Jane"
        assert updated_user["is_active"] is False
        assert "last_updated" in updated_user
        assert user_repository.get_user_by_id(1) == updated_user

    def test_update_user_returns_none_for_unknown_user(self, user_repository):
        assert user_repository.update_user(999, {"firstname": "Nobody"}) is None

    def test_get_all_users_raises_for_missing_file(self, tmp_path):
        repository = UserRepository(tmp_path / "missing.json")

        with pytest.raises(FileNotFoundError, match="File not found"):
            repository.get_all_users()

    def test_get_all_users_raises_for_invalid_json(self, tmp_path):
        invalid_file = tmp_path / "invalid.json"
        invalid_file.write_text("not valid json")
        repository = UserRepository(invalid_file)

        with pytest.raises(ValueError, match="not valid JSON"):
            repository.get_all_users()

    def test_save_users_raises_for_unserializable_data(self, user_repository):
        with pytest.raises(OSError, match="Error saving data"):
            user_repository.save_users({"users": object()})