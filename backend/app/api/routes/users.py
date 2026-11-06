from app.schemas.error import ErrorResponse
from app.schemas.user import User, UserCreate, UserUpdate
from fastapi import APIRouter, Depends, HTTPException, Path, status

from backend.app.repositories.user_repository import UserRepository
from backend.app.services.user_service import UserService

router = APIRouter()
UserId = Path(description="ID of the user")

def get_user_service() -> UserService:
    return UserService(UserRepository())

user_service_dependency = Depends(get_user_service)

@router.get(
    "/users",
    tags=["Users"],
    summary="List all users",
    description="Returns a list of all users.",
    status_code=status.HTTP_200_OK,
    response_model=list[dict],
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "User data could not be read",
        }
    },
)
def get_users(user_service: UserService = user_service_dependency):
    return user_service.get_all_users()

@router.post(
    "/users",
    tags=["Users"],
    summary="Create a user",
    description="Creates a user with the provided details and returns it with its new ID.",
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
    responses={400: {"model": ErrorResponse, "description": "Invalid user details"}},
)
def create_user(user: UserCreate, user_service: UserService = user_service_dependency):
    try:
        return user_service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put(
    "/users/{user_id}",
    tags=["Users"],
    summary="Update a user",
    description="Partially updates a user: only the fields sent are changed.",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "User not found",
        }
    },
)
def update_user(
    update_data: UserUpdate,
    user_id: int = UserId,
    user_service: UserService = user_service_dependency,
):
    try:
        return user_service.update_user(user_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put(
    "/users/{user_id}/deactivate",
    tags=["Users"],
    summary="Deactivate a user",
    description="Deactivates a user. Deactivated users cannot log in.",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "User not found",
        }
    },
)
def deactivate_user(
    user_id: int = UserId,
    user_service: UserService = user_service_dependency,
):
    try:
        return user_service.deactivate_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get(
    "/users/{user_id}",
    tags=["Users"],
    summary="Get user details",
    description="Returns one user's details.",
    status_code=status.HTTP_200_OK,
    response_model=User,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "User not found",
        }
    },
)
def view_user(
    user_id: int = UserId,
    user_service: UserService = user_service_dependency,
):
    try:
        return user_service.view_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))