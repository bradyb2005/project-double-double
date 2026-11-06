from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    price: float
    category: str
    image: str #Need to figure out how to validate only image urls
    availability: bool = True
    description: str | None = None

class ItemRead(ItemCreate):
    id: int

class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    category: str | None = None
    image: str | None = None
    availability: bool | None = None
    description: str | None = None

# update_menu_item returns only the id plus the fields that were changed
class ItemUpdated(ItemUpdate):
    id: int
