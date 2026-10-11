from fastapi import APIRouter, HTTPException, status
from app.schemas.restaurant import RestaurantCreate, RestaurantRead
from app.services.restaurant_service import RestaurantService

router = APIRouter()
service = RestaurantService()

@router.get("/health")
def health_check():
    return {"status": "healthy"}

@router.get("/restaurants", response_model=list[RestaurantRead])
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
    
@router.get("/restaurants/{id}", response_model=RestaurantRead)
def get_restaurant_details(id: int):
    try:
        return service.fetch_restaurant_details(id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

