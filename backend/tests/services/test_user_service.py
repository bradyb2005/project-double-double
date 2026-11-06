import pytest
from pydantic import ValidationError

from backend.app.schemas.user import Address, Province, UserRole


def test_get_all_users_returns_repository_users(user_service):
    users = user_service.get_all_users()

    assert len(users) == 1
    assert users[0]["email"] == "john.doe@example.com"


def test_create_user_defaults_to_customer_and_generates_stored_fields(
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
    assert "last_modified" in created_user

    persisted_user = user_service.view_user(created_user["id"])
    assert persisted_user == created_user


def test_create_user_allows_restaurant_role(user_service, valid_user_create):
    valid_user_create.role = UserRole.RESTAURANT

    created_user = user_service.create_user(valid_user_create)

    assert created_user["role"] == "restaurant"


def test_view_user_returns_profile_details(user_service):
    user = user_service.view_user(1)

    assert user["id"] == 1
    assert user["firstname"] == "John"
    assert user["address"]["city"] == "Kelowna"


def test_view_user_raises_for_missing_user(user_service):
    with pytest.raises(ValueError, match="User not found"):
        user_service.view_user(999)


def test_update_user_changes_personal_information_and_address(
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


def test_update_user_preserves_fields_not_in_update(user_service, valid_user_update):
    original_user = user_service.view_user(1)

    user_service.update_user(1, valid_user_update)
    updated_user = user_service.view_user(1)

    assert updated_user["lastname"] == original_user["lastname"]
    assert updated_user["email"] == original_user["email"]


def test_update_user_raises_for_missing_user(user_service, valid_user_update):
    with pytest.raises(ValueError, match="User not found"):
        user_service.update_user(999, valid_user_update)


def test_deactivate_user_sets_account_inactive(user_service):
    deactivated_user = user_service.deactivate_user(1)

    assert deactivated_user["is_active"] is False
    assert user_service.view_user(1)["is_active"] is False


def test_deactivate_user_raises_for_missing_user(user_service):
    with pytest.raises(ValueError, match="User not found"):
        user_service.deactivate_user(999)


def test_deactivate_user_raises_when_already_deactivated(user_service):
    user_service.deactivate_user(1)

    with pytest.raises(ValueError, match="already deactivated"):
        user_service.deactivate_user(1)


def test_user_create_rejects_invalid_profile_data(valid_user_payload):
    from app.schemas.user import UserCreate

    invalid_payload = {**valid_user_payload, "email": "not-an-email"}

    with pytest.raises(ValidationError):
        UserCreate(**invalid_payload)