from app.schemas.error import ErrorResponse
from app.schemas.user import LoginRequest, LoginResponse
from fastapi import APIRouter, Depends, HTTPException, status

from app.repositories.user_repository import UserRepository
from app.services.login_service import LoginService

router = APIRouter()

def get_login_service() -> LoginService:
    return LoginService(UserRepository())

login_service_dependency = Depends(get_login_service)

@router.post(
    "/login",
    tags=["Login"],
    summary="Sign in",
    description="Authenticates a user and returns a bearer access token.",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Invalid email or password",
        }
    },
)
def login(
    credentials: LoginRequest,
    login_service: LoginService = login_service_dependency,
):
    try:
        return login_service.login(credentials)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        ) from error