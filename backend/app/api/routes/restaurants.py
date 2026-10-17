from fastapi import APIRouter, Depends, HTTPException, Path, status
from app.schemas.error import ErrorResponse, HealthStatus
from app.schemas.restaurant import RestaurantCreate, RestaurantFilter, RestaurantRead, RestaurantUpdate, RestaurantWithMenu
from app.services.restaurant_service import RestaurantService
from app.schemas.menu_item import ItemCreate, ItemRead, ItemUpdate, ItemUpdated

router = APIRouter()
service = RestaurantService()

RestaurantId = Path(description="ID of the restaurant")
ItemId = Path(description="ID of the menu item, unique within its restaurant")

@router.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    description="Returns HTTP 200 with `{\"status\": \"healthy\"}` while the API is running.",
    response_model=HealthStatus,
)
def health_check():
    return {"status": "healthy"}

@router.get(
    "/restaurants",
    tags=["Restaurants"],
    summary="List, search and filter restaurants",
    description=(
        "Returns every restaurant, including its embedded menu. "
        "All query parameters are optional and combine with AND. "
        "`search` matches the name or cuisine (case-insensitive substring), "
        "`cuisine`, `city` and `province` match exactly (case-insensitive), "
        "and `rating` is a minimum."
    ),
    response_model=list[RestaurantWithMenu],
    responses={400: {"model": ErrorResponse, "description": "Invalid search or filter"}},
)
def get_restaurants(filter: RestaurantFilter = Depends()):
    try:
        return service.search_and_filter_restaurants(filter)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post(
    "/restaurants",
    tags=["Restaurants"],
    summary="Create a restaurant",
    description=(
        "Creates a restaurant with an empty menu and returns it with its new ID. "
        "The phone number, if given, must be `###-###-####` or `##########`, "
        "and the postal code must be a Canadian postal code such as `V1V 1V7`."
    ),
    status_code=status.HTTP_201_CREATED,
    response_model=RestaurantWithMenu,
    responses={400: {"model": ErrorResponse, "description": "Empty required field, bad phone number or bad postal code"}},
)
def create_restaurant(restaurant: RestaurantCreate):
    try:
        return service.create_restaurant(restaurant)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get(
    "/restaurants/{restaurant_id}/menu",
    tags=["Menu"],
    summary="Get a restaurant's menu",
    description="Returns all menu items of one restaurant. The list is empty if the restaurant has no items yet.",
    response_model=list[ItemRead],
    responses={404: {"model": ErrorResponse, "description": "Restaurant not found"}},
)
def get_menu_items(restaurant_id: int = RestaurantId):
    try:
        return service.fetch_restaurant_menu(restaurant_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post(
    "/restaurants/{restaurant_id}/menu",
    tags=["Menu"],
    summary="Add a menu item",
    description=(
        "Adds an item to a restaurant's menu and returns it with its new ID. "
        "The price must be greater than 0 and the category must be one of the allowed menu categories "
        "(for example Starters, Mains, Dessert or Drinks)."
    ),
    status_code=status.HTTP_201_CREATED,
    response_model=ItemRead,
    responses={400: {"model": ErrorResponse, "description": "Restaurant not found, empty name, price not above 0 or invalid category"}},
)
def create_menu_item(item: ItemCreate, restaurant_id: int = RestaurantId):
    try:
        return service.create_menu_item(restaurant_id, item)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put(
    "/restaurants/{restaurant_id}/menu/{item_id}",
    tags=["Menu"],
    summary="Update a menu item",
    description=(
        "Partially updates a menu item: only the fields sent are changed. "
        "Returns the item ID and the fields that were updated."
    ),
    response_model=ItemUpdated,
    response_model_exclude_unset=True,
    responses={400: {"model": ErrorResponse, "description": "Restaurant or item not found, or an invalid value (empty name, price not above 0, invalid category)"}},
)
def update_menu_item(item: ItemUpdate, restaurant_id: int = RestaurantId, item_id: int = ItemId):
    try:
        return service.update_menu_item(restaurant_id,item_id,item)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

# /restaurants/names must be defined before /restaurants/{id}, or "names" is parsed as an id
@router.get(
    "/restaurants/names",
    tags=["Restaurants"],
    summary="List restaurant names",
    description="Returns only the names of all restaurants.",
    response_model=list[str],
    responses={400: {"model": ErrorResponse, "description": "Restaurant data could not be read"}},
)
def get_all_restaurant_names():
    try:
        return service.fetch_all_restaurant_names()
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put(
    "/restaurants/update/{restaurant_id}",
    tags=["Restaurants"],
    summary="Update a restaurant",
    description=(
        "Partially updates a restaurant: only the fields sent are changed, and blank strings are ignored. "
        "Returns the full updated restaurant. The menu cannot be changed here, use the menu endpoints."
    ),
    status_code=status.HTTP_200_OK,
    response_model=RestaurantWithMenu,
    responses={404: {"model": ErrorResponse, "description": "Restaurant not found, or the phone number or postal code is invalid"}},
)
def update_restaurant_by_id(restaurant: RestaurantUpdate, restaurant_id: int = RestaurantId):
    try:
        return service.update_restaurant(restaurant_id, restaurant)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get(
    "/restaurants/{id}",
    tags=["Restaurants"],
    summary="Get restaurant details",
    description="Returns one restaurant's details (without its menu, see the menu endpoint).",
    response_model=RestaurantRead,
    responses={404: {"model": ErrorResponse, "description": "Restaurant not found"}},
)
def get_restaurant_details(id: int = Path(description="ID of the restaurant")):
    try:
        return service.fetch_restaurant_details(id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
