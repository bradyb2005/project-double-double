from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.menu_item import ItemRead

class Location(BaseModel):
    city: str
    province: str

class RestaurantCreate(BaseModel):
    name: str
    cuisine: Optional[str] = None
    phone: Optional[str] = None
    address: str
    postalcode: str
    location: Location

# Update restaurant. All optional and will fall back. Id required to look up correct restaurant^^
class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    cuisine: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    postalcode: Optional[str] = None
    location: Optional[Location] = None
class RestaurantRead(BaseModel):
    id: int
    name: str
    cuisine: Optional[str] = None
    phone: Optional[str] = None
    address: str
    postalcode: str
    location: Location
    rating: Optional[float] = 0.0

class RestaurantWithMenu(RestaurantRead):
    menu: list[ItemRead] = Field(default_factory=list, description="Menu items embedded in the restaurant")

class RestaurantFilter(BaseModel):
    search: Optional[str] = Field(default=None, description="Search term for restaurant name or cuisine")
    cuisine: Optional[str] = Field(default=None, description="Type of cuisine restaurant serves")
    city: Optional[str] = Field(default=None, description="City location")
    province: Optional[str] = Field(default=None, description="Province location")
    rating: Optional[float] = Field(default=None, description="Minimum rating")
