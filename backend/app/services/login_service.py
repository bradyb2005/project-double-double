from app.core.security import create_access_token, verify_password
from app.schemas.user import LoginRequest, LoginResponse


class LoginService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def login(self, credentials: LoginRequest) -> LoginResponse:
        user = self.user_repository.get_user_by_email(credentials.email)

        if (
            user is None
            or user.get("is_active") is False
            or not verify_password(
                credentials.password,
                user.get("password_hash", ""),
            )
        ):
            raise ValueError("Invalid email or password")

        return LoginResponse(
            access_token=create_access_token(user["id"]),
        )