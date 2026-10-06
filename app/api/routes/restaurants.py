from fastapi import APIRouter, HTTPException, status
from app.schemas.restaurant import RestaurantCreate
from app.services.restaurant_service import RestaurantService
from app.schemas.menu_item import ItemCreate

router = APIRouter()
service = RestaurantService()

@router.get("/health")
def health_check():
    return {"status": "healthy"}

@router.get("/restaurants")
def get_restaurants():
    return service.fetch_restaurant_list()

@router.post("/restaurants", status_code=status.HTTP_201_CREATED)
def create_restaurant(restaurant: RestaurantCreate):
    try:
        return service.create_restaurant(restaurant)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/restaurants/{restaurant_id}/menu", status_code=status.HTTP_201_CREATED)
def create_menu_item(restaurant_id: int, item: ItemCreate):
    try:
        return service.create_menu_item(restaurant_id, item)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))