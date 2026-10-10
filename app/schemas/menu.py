from pydantic import BaseModel


class MenuRead(BaseModel):
    id: int
    restaurant_id: int
    category: str
    name: str
    description:str
    price: float