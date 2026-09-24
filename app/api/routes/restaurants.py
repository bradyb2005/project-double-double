from fastapi import APIRouter
from app.services.restaurant_service import RestaurantService

router = APIRouter()
service = RestaurantService()

@router.get("/health")
def healthCheck():
    return {"status": "healthy"}

@router.get("/restaurants")
def getRestaurants():
    return service.fetchRestaurantList()
