from app.core.dependencies import require_same_user
from app.schemas.error import ErrorResponse
from app.schemas.order import Order
from app.services.order_service import OrderService
from fastapi import APIRouter, Depends, HTTPException, Path, status

router = APIRouter()

UserId = Path(description="ID of the customer")

def get_order_service() -> OrderService:
    return OrderService()

order_service_dependency = Depends(get_order_service)
same_user_dependency = Depends(require_same_user)


@router.post(
    "/users/{user_id}/orders/checkout",
    tags=["Orders"],
    summary="Checkout user's order",
    description="Submits the user's order for processing.",
    status_code=status.HTTP_201_CREATED,
    response_model=Order,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Invalid quantity or order placing failed",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "User, restaurant, or menu item not found",
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Authentication required"},
        status.HTTP_403_FORBIDDEN: {"description": "Own cart access required"},
    },
)

def checkout(
    user_id: int = UserId,
    current_user = same_user_dependency,
    order_service: OrderService = order_service_dependency,
):
    try:
        return order_service.checkout(user_id)
    except ValueError as e:
        message = str(e)
        if "not found" in message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
        if "no longer exists" in message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )


@router.get(
    "/users/{user_id}/orders",
    tags=["Orders"],
    summary="List user's orders",
    description="Returns every order the user has placed, current and past, newest first.",
    status_code=status.HTTP_200_OK,
    response_model=list[Order],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Authentication required"},
        status.HTTP_403_FORBIDDEN: {"description": "Own orders access required"},
    },
)
def list_orders(
    user_id: int = UserId,
    current_user = same_user_dependency,
    order_service: OrderService = order_service_dependency,
):
    return order_service.get_customer_orders(user_id)


@router.get(
    "/users/{user_id}/orders/{order_id}",
    tags=["Orders"],
    summary="Get one of the user's orders",
    description="Returns a single order with its status, items, snapshot prices and total, if the user placed it.",
    status_code=status.HTTP_200_OK,
    response_model=Order,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Order not found for this user",
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Authentication required"},
        status.HTTP_403_FORBIDDEN: {"description": "Own orders access required"},
    },
)
def get_order(
    user_id: int = UserId,
    order_id: int = Path(description="ID of the order"),
    current_user = same_user_dependency,
    order_service: OrderService = order_service_dependency,
):
    try:
        return order_service.get_customer_order(user_id, order_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))





