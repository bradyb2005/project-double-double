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
    search: str | None = Field(None, description="Search term for restaurant name or cuisine")
    cuisine: str | None = Field(None, description="Type of cuisine restaurant serves")
    city: str | None = Field(None, description="City location")
    province: str | None = Field(None, description="Province location")
    rating: float | None = Field(None, description="Minimum rating")