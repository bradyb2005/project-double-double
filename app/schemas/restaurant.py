from typing import Optional
from pydantic import BaseModel, Field

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

class RestaurantFilter(BaseModel):
    search: Optional[str] = None
    cuisine: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    rating: Optional[float] = None