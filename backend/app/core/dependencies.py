from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.app.core.security import decode_access_token
from backend.app.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer(auto_error=False)
bearer_credentials_dependency = Depends(bearer_scheme)


def get_user_repository() -> UserRepository:
    return UserRepository()


user_repository_dependency = Depends(get_user_repository)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = bearer_credentials_dependency,
    user_repository: UserRepository = user_repository_dependency,
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = decode_access_token(credentials.credentials)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        ) from error

    user = user_repository.get_user_by_id(user_id)
    if user is None or user.get("is_active") is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive account",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


current_user_dependency = Depends(get_current_user)


def require_role(required_role: str):
    def role_dependency(current_user=current_user_dependency):
        if current_user.get("role") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )
        return current_user

    return role_dependency


def require_same_user(user_id: int, current_user=current_user_dependency):
    if current_user.get("id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own profile",
        )
    return current_user
