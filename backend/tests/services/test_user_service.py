import pytest
from app.core.security import get_password_hash, verify_password
from app.schemas.user import Address, Province, UserRole
from pydantic import ValidationError


class TestGetAllUsers:
    def test_get_all_users_returns_repository_users(self, user_service):
        users = user_service.get_all_users()

        assert len(users) == 1
        assert users[0]["email"] == "john.doe@example.com"

class TestCreateUser:
    def test_create_user_defaults_to_customer_and_generates_stored_fields(self,
        user_service, valid_user_create
    ):
        created_user = user_service.create_user(valid_user_create)

        assert created_user["id"] == 2
        assert created_user["role"] == "customer"
        assert created_user["is_active"] is True
        assert created_user["email"] == valid_user_create.email
        assert created_user["password_hash"] != valid_user_create.password
        assert "password" not in created_user
        assert "created_at" in created_user
        assert "last_updated" in created_user

        persisted_user = user_service.view_user(created_user["id"])
        assert persisted_user == created_user

    def test_create_user_allows_restaurant_role(self, user_service, valid_user_create):
        valid_user_create.role = UserRole.RESTAURANT

        created_user = user_service.create_user(valid_user_create)

        assert created_user["role"] == "restaurant"

class TestViewUser:
    def test_view_user_returns_profile_details(self, user_service):
        user = user_service.view_user(1)

        assert user["id"] == 1
        assert user["firstname"] == "John"
        assert user["address"]["city"] == "Kelowna"

    def test_view_user_raises_for_missing_user(self, user_service):
        with pytest.raises(ValueError, match="User not found"):
            user_service.view_user(999)

class TestUpdateUser:
    def test_update_user_changes_personal_information_and_address(self,
        user_service, valid_user_update
    ):
        valid_user_update.address = Address(
            street="200 New Street",
            city="Vancouver",
            province=Province.BC,
            postalcode="V6B 1A1",
        )

        updated_user = user_service.update_user(1, valid_user_update)

        assert updated_user["firstname"] == "UpdatedName"
        assert updated_user["is_active"] is False
        assert updated_user["address"]["street"] == "200 New Street"
        assert updated_user["address"]["postalcode"] == "V6B1A1"

    def test_update_user_preserves_fields_not_in_update(self, user_service, valid_user_update):
        original_user = user_service.view_user(1)

        user_service.update_user(1, valid_user_update)
        updated_user = user_service.view_user(1)

        assert updated_user["lastname"] == original_user["lastname"]
        assert updated_user["email"] == original_user["email"]

    def test_update_user_raises_for_missing_user(self, user_service, valid_user_update):
        with pytest.raises(ValueError, match="User not found"):
            user_service.update_user(999, valid_user_update)

class TestDeactivateUser:
    def test_deactivate_user_sets_account_inactive(self, user_service):
        deactivated_user = user_service.deactivate_user(1)

        assert deactivated_user["is_active"] is False
        assert user_service.view_user(1)["is_active"] is False

    def test_deactivate_user_raises_for_missing_user(self, user_service):
        with pytest.raises(ValueError, match="User not found"):
            user_service.deactivate_user(999)

    def test_deactivate_user_raises_when_already_deactivated(self, user_service):
        user_service.deactivate_user(1)

        with pytest.raises(ValueError, match="already deactivated"):
            user_service.deactivate_user(1)

class TestUserCreateSchema:
    def test_user_create_rejects_invalid_profile_data(self, valid_user_payload):
        from app.schemas.user import UserCreate

        invalid_payload = {**valid_user_payload, "email": "not-an-email"}

        with pytest.raises(ValidationError):
            UserCreate(**invalid_payload)

    def test_user_create_defaults_and_normalizes_optional_fields(self):
        from app.schemas.user import UserCreate

        user = UserCreate(
            firstname="Jane",
            lastname="Doe",
            email="jane.doe@example.com",
            phone="2505550100",
            password="SecurePassword123!",
        )

        assert user.role is UserRole.CUSTOMER
        assert user.is_active is True
        assert user.phone == "2505550100"
        assert user.address is None

    @pytest.mark.parametrize(
        "overrides",
        [
            {"firstname": None},
            {"lastname": None},
            {"email": "invalid-email"},
            {"phone": "123"},
            {"password": "short"},
        ],
    )
    def test_user_create_rejects_missing_or_invalid_profile_data(self, valid_user_payload, overrides):
        from app.schemas.user import UserCreate

        payload = {**valid_user_payload, **overrides}

        with pytest.raises(ValidationError):
            UserCreate(**payload)

class TestPasswordHash:
    def test_password_hash_verification(self):
        password = "SecurePassword123!"
        password_hash = get_password_hash(password)

        assert verify_password(password, password_hash) is True
        assert verify_password("WrongPassword123!", password_hash) is False

    def test_create_user_with_empty_repository_starts_at_id_one(self, tmp_path, valid_user_create):
        from app.repositories.user_repository import UserRepository
        from app.services.user_service import UserService

        empty_file = tmp_path / "empty-users.json"
        empty_file.write_text("[]")
        service = UserService(UserRepository(empty_file))

        created_user = service.create_user(valid_user_create)

        assert created_user["id"] == 1

    def test_update_user_refreshes_last_updated_timestamp(self, user_service, valid_user_update):
        original_timestamp = user_service.view_user(1)["last_updated"]

        updated_user = user_service.update_user(1, valid_user_update)

        assert updated_user["last_updated"] != original_timestamp