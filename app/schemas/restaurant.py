from typing import Optional
from pydantic import BaseModel

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
    
class RestaurantRead(BaseModel):
    id: int
    name: str
    cuisine: Optional[str] = None
    phone: Optional[str] = None
    address: str
    postalcode: str
    location: Location
    rating: str