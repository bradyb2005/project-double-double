from fastapi import APIRouter, HTTPException

from backend.app.repositories.user_repository import UserRepository
from backend.app.schemas.user import User
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