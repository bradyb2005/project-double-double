from fastapi import APIRouter, HTTPException, status

from backend.app.repositories.user_repository import UserRepository
from backend.app.schemas.user import User, UserCreate, UserUpdate
from backend.app.services.user_service import UserService

router = APIRouter()
service = UserService(UserRepository())

@router.get(
    "/users",
    tags=["Users"],
    summary="List all users",
    description="Returns a list of all users.",
    response_model=list[dict],
)
def get_users():
    return service.get_all_users()

@router.post(
    "/users",
    tags=["Users"],
    summary="Create a new user",
    description="Creates a new user with the provided details.",
    status_code=201,
    response_model=dict,
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
    description="Updates the details of a specific user.",
    response_model=dict,
)
def update_user(user_id: int, update_data: UserUpdate):
    try:
        return service.update_user(user_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get(
    "/users/{user_id}",
    tags=["Users"],
    summary="View a user",
    description="Returns the details of a specific user.",
    response_model=User,
)
def view_user(user_id: int):
    try:
        return service.view_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))