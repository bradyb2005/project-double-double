from fastapi import APIRouter, HTTPException, Path, status

from backend.app.repositories.user_repository import UserRepository
from backend.app.schemas.error import ErrorResponse
from backend.app.schemas.user import User, UserCreate, UserUpdate
from backend.app.services.user_service import UserService

router = APIRouter()
service = UserService(UserRepository())
UserId = Path(description="ID of the user")


@router.get(
    "/users",
    tags=["Users"],
    summary="List all users",
    description="Returns a list of all users.",
    response_model=list[dict],
    responses={400: {"model": ErrorResponse, "description": "User data could not be read"}},
)
def get_users():
    return service.get_all_users()


@router.post(
    "/users",
    tags=["Users"],
    summary="Create a user",
    description="Creates a user with the provided details and returns it with its new ID.",
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
    responses={400: {"model": ErrorResponse, "description": "Invalid user details"}},
)
def create_user(user: UserCreate):
    try:
        return service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put(
    "/users/{user_id}",
    tags=["Users"],
    summary="Update a user",
    description="Partially updates a user: only the fields sent are changed.",
    response_model=dict,
    responses={404: {"model": ErrorResponse, "description": "User not found"}},
)
def update_user(update_data: UserUpdate, user_id: int = UserId):
    try:
        return service.update_user(user_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/users/{user_id}",
    tags=["Users"],
    summary="Get user details",
    description="Returns one user's details.",
    response_model=User,
    responses={404: {"model": ErrorResponse, "description": "User not found"}},
)
def view_user(user_id: int = UserId):
    try:
        return service.view_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))