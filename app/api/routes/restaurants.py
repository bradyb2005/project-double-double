from fastapi import APIRouter
from app.services.restaurant_service import RestaurantService

router = APIRouter()
service = RestaurantService()

@router.get("/health")
def health_check():
    return {"status": "healthy"}

@router.get("/restaurants")
def get_restaurants():
    return service.fetch_restaurant_list()

@router.post("/restaurants")
def create_restaurant(restaurant: dict):
    from app.schemas.restaurant import RestaurantCreate
    restaurant_create = RestaurantCreate(**restaurant)
    return service.create_restaurant(restaurant_create)