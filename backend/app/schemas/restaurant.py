from app.schemas.menu_item import ItemRead
from pydantic import BaseModel, Field


class Location(BaseModel):
    city: str
    province: str

class RestaurantCreate(BaseModel):
    name: str
    cuisine: str | None = None
    phone: str | None = None
    address: str
    postalcode: str
    location: Location

# Update restaurant. All optional and will fall back. Id required to look up correct restaurant^^
class RestaurantUpdate(BaseModel):
    name: str | None = None
    cuisine: str | None = None
    phone: str | None = None
    address: str | None = None
    postalcode: str | None = None
    location: str | None = None
class RestaurantRead(BaseModel):
    id: int
    name: str
    cuisine: str | None = None
    phone: str | None = None
    address: str
    postalcode: str
    location: Location
    rating: float | None = 0.0

class RestaurantWithMenu(RestaurantRead):
    menu: list[ItemRead] = Field(default_factory=list, description="Menu items embedded in the restaurant")

class RestaurantFilter(BaseModel):
    search: str | None = Field(default=None, description="Search term for restaurant name or cuisine")
    cuisine: str | None = Field(default=None, description="Type of cuisine restaurant serves")
    city: str | None = Field(default=None, description="City location")
    province: str | None = Field(default=None, description="Province location")
    rating: float | None = Field(default=None, description="Minimum rating")
