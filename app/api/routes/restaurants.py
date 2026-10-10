from fastapi import APIRouter, HTTPException, status
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate
from app.services.restaurant_service import RestaurantService

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

@router.get("/restaurants/names")
def get_all_restaurant_names():
    try:
        return service.fetch_all_restaurant_names()
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/restaurants/update/{restaurant_id}", status_code=status.HTTP_200_OK)
def update_restaurant_by_id(restaurant_id: int, restaurant: RestaurantUpdate):
    try:
        return service.update_restaurant(restaurant_id, restaurant)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))