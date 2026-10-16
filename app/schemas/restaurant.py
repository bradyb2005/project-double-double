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

class RestaurantRead(BaseModel):
    id: int
    name: str
    cuisine: Optional[str] = None
    phone: Optional[str] = None
    address: str
    postalcode: str
    location: Location
    rating: Optional[float] = 0.0

class RestaurantFilter(BaseModel):
    search: Optional[str] = Field(default=None, description="Search term for restaurant name or cuisine")
    cuisine: Optional[str] = Field(default=None, description="Type of cuisine restaurant serves")
    city: Optional[str] = Field(default=None, description="City location")
    province: Optional[str] = Field(default=None, description="Province location")
    rating: Optional[float] = Field(default=None, description="Minimum rating")
