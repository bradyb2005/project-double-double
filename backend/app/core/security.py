import os
from datetime import UTC, datetime, timedelta
from importlib import import_module
from pathlib import Path

from dotenv import load_dotenv
from passlib.context import CryptContext

jwt = import_module("jwt")
InvalidTokenError = jwt.InvalidTokenError

load_dotenv(Path(__file__).resolve().parents[3] / ".env")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def _get_jwt_secret() -> str:
    secret = os.getenv("SECRET_KEY")
    if not secret:
        raise RuntimeError("SECRET_KEY must be configured to use access tokens")
    return secret


def get_password_hash(password: str) -> str:
    """Takes a plain text password and returns a hashed string."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if a plain text password matches the stored hashed version."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    user_id: int,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a signed bearer token containing the user's ID."""
    expires_at = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {"sub": str(user_id), "exp": expires_at}
    return jwt.encode(payload, _get_jwt_secret(), algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> int:
    """Validate a bearer token and return the user ID it contains."""
    try:
        payload = jwt.decode(
            token,
            _get_jwt_secret(),
            algorithms=[JWT_ALGORITHM],
            options={"require": ["sub", "exp"]},
        )
        return int(payload["sub"])
    except (InvalidTokenError, KeyError, TypeError, ValueError) as error:
        raise ValueError("Invalid or expired access token") from error