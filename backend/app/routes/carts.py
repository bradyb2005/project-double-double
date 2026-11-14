from app.core.dependencies import require_same_user
from app.schemas.cart import Cart, CartItem
from app.schemas.error import ErrorResponse
from app.services.cart_service import CartService
from fastapi import APIRouter, Depends, HTTPException, Path, status

router = APIRouter()
UserId = Path(description="ID of the user")


def get_cart_service() -> CartService:
    return CartService()


cart_service_dependency = Depends(get_cart_service)
same_user_dependency = Depends(require_same_user)


@router.get(
    "/users/{user_id}/cart",
    tags=["Cart"],
    summary="Get user's cart",
    description="Retrieves the shopping cart for a specific user.",
    status_code=status.HTTP_200_OK,
    response_model=Cart,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "User not found",
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Authentication required"},
        status.HTTP_403_FORBIDDEN: {"description": "Own cart access required"},
    },
)
def get_cart(
    user_id: int = UserId,
    current_user=same_user_dependency,
    cart_service: CartService = cart_service_dependency,
):
    try:
        return cart_service.get_cart(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post(
    "/users/{user_id}/cart/items",
    tags=["Cart"],
    summary="Add item to cart",
    description="Adds an item to the user's shopping cart.",
    status_code=status.HTTP_200_OK,
    response_model=Cart,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Invalid item data or cart operation failed",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "User, restaurant, or menu item not found",
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Authentication required"},
        status.HTTP_403_FORBIDDEN: {"description": "Own cart access required"},
    },
)
def add_to_cart(
    item: CartItem,
    user_id: int = UserId,
    current_user=same_user_dependency,
    cart_service: CartService = cart_service_dependency,
):
    try:
        return cart_service.add_to_cart(
            user_id, item.item_id, item.restaurant_id, item.quantity
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put(
    "/users/{user_id}/cart/items/{item_id}",
    tags=["Cart"],
    summary="Update cart item quantity",
    description="Updates the quantity of an item in the user's cart.",
    status_code=status.HTTP_200_OK,
    response_model=Cart,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Invalid quantity or cart operation failed",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "User or item not found in cart",
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Authentication required"},
        status.HTTP_403_FORBIDDEN: {"description": "Own cart access required"},
    },
)
def update_cart_item(
    user_id: int = UserId,
    item_id: int = Path(description="ID of the item in cart"),
    quantity: int = Path(..., gt=0, description="New quantity (must be > 0)"),
    current_user=same_user_dependency,
    cart_service: CartService = cart_service_dependency,
):
    try:
        return cart_service.update_cart_item(user_id, item_id, quantity)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/users/{user_id}/cart/items/{item_id}",
    tags=["Cart"],
    summary="Remove item from cart",
    description="Removes an item from the user's shopping cart.",
    status_code=status.HTTP_200_OK,
    response_model=Cart,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "User not found",
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Authentication required"},
        status.HTTP_403_FORBIDDEN: {"description": "Own cart access required"},
    },
)
def remove_from_cart(
    user_id: int = UserId,
    item_id: int = Path(description="ID of the item to remove"),
    current_user=same_user_dependency,
    cart_service: CartService = cart_service_dependency,
):
    try:
        return cart_service.remove_from_cart(user_id, item_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/users/{user_id}/cart",
    tags=["Cart"],
    summary="Clear user's cart",
    description="Clears all items from the user's shopping cart.",
    status_code=status.HTTP_200_OK,
    response_model=Cart,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "User not found",
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Authentication required"},
        status.HTTP_403_FORBIDDEN: {"description": "Own cart access required"},
    },
)
def clear_cart(
    user_id: int = UserId,
    current_user=same_user_dependency,
    cart_service: CartService = cart_service_dependency,
):
    try:
        return cart_service.clear_cart(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
