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
