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

# Update restaurant. All optional and will fall back. Id required to look up correct restaurant^^
class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    cuisine: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    postalcode: Optional[str] = None
    location: Optional[Location] = None