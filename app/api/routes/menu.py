from fastapi import APIRouter, HTTPException, status
from app.schemas.menu import MenuRead
from app.services.menu_service import MenuService


menu_router = APIRouter()
service = MenuService()

@menu_router.get("/restaurants/{id}/menu", response_model=list[MenuRead])
def get_menu_items(id: int):
    try:
        return service.fetch_restaurant_menu(id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))